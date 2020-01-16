import json
from apps.utils import data
from apps.db import queries
from apps.db.DBHandler import DBHandler


JSON_PATH = '../../data/json/'
CURR_SESSION = '116'


def process_congress_session_json(dbh, files):
    for file in files:
        print("Processing: " + file)

        with open(JSON_PATH + file) as json_file:
            district_id = None

            json_data = json.load(json_file)

            session_num = json_data["results"][0]["congress"]
            chamber = json_data["results"][0]["chamber"]

            for member_record in json_data["results"][0]["members"]:
                member = data.convert_empty_to_null(member_record)
                if not member["id"]:
                    raise ValueError

                if chamber == "House" and member["district"] == "At-Large":
                    member["district"] = 0
                if chamber == "Senate":
                    member["district"] = None
                if chamber == "House":
                    district_id = dbh.query_db(queries.get_district(),
                                               (member["state"], member["district"]))[0]
                if "votes_against_party_pct" not in member:
                    member["votes_against_party_pct"] = None
                if "missed_votes_pct" not in member:
                    member["missed_votes_pct"] = None
                if "votes_with_party_pct" not in member:
                    member["votes_with_party_pct"] = None
                if "next_election" not in member:
                    member["next_election"] = None
                if "party" in member and len(member["party"]) > 1:
                    # Some independents are marked with "ID" instead of "I"
                    member["party"] = member["party"][0]

                member_id_val = (member["id"],)

                member_vals = (member["id"], member["in_office"], member["first_name"],
                               member["middle_name"], member["last_name"],
                               member["suffix"], member["date_of_birth"],
                               member["gender"])

                member_session_vals = (
                    member["id"], session_num, chamber, member["state"],
                    member["district"], district_id, member["party"],
                    member["dw_nominate"], member["total_votes"],
                    member["missed_votes"], member["total_present"],
                    member["missed_votes_pct"], member["votes_with_party_pct"],
                    member["votes_against_party_pct"], member["office"],
                    member["next_election"], member["last_updated"])

                ids_vals = (
                    member["id"], member["govtrack_id"], member["cspan_id"],
                    member["votesmart_id"], member["icpsr_id"], member["crp_id"],
                    member["google_entity_id"], member["fec_candidate_id"],
                    member["rss_url"],
                    member["url"], member["youtube_account"],
                    member["facebook_account"], member["twitter_account"])

                count = dbh.query_db(queries.get_count_in_member(),
                                     (member["id"],), True)

                if count[0] == 0:
                    dbh.write_to_db(queries.insert_member(), member_vals)

                count_ms = dbh.query_db(
                    queries.get_count_in_member_session(),
                    (member["id"], session_num, member["party"]), True)

                if count_ms[0] == 0:
                    dbh.write_to_db(queries.insert_member_session(), member_session_vals)

                if session_num == CURR_SESSION and count[0] == 0:
                    dbh.write_to_db(queries.insert_member_codes_ids(), ids_vals)

                    if chamber == "Senate":
                        dbh.write_to_db(queries.insert_member_senate(), member_id_val)
                    else:
                        dbh.write_to_db(queries.insert_current_to_member_district(),
                                        (member["id"], district_id))
                        dbh.write_to_db(queries.insert_member_house(), member_id_val)

                        if member["cook_pvi"]:
                            dbh.write_to_db(queries.insert_district_summary(),
                                            (district_id, member["cook_pvi"]))

        print("committed rows for " + file + "!")


def main():
    dbh = DBHandler()

    senate_files = [
        '116th-senate.json',
        '115th-senate.json',
        '114th-senate.json',
        '113th-senate.json',
        '112th-senate.json',
        '111th-senate.json']

    house_files = [
        '116th-house.json',
        '115th-house.json',
        '114th-house.json',
        '113th-house.json',
        '112th-house.json',
        '111th-house.json']

    process_congress_session_json(dbh, house_files)
    process_congress_session_json(dbh, senate_files)
    dbh.close()


if __name__ == "__main__":
    main()
