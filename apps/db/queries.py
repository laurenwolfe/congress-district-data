############
# SELECTS
############


def get_member_id_by_current_district():
    sql = """
        SELECT member_id
        from member_district
        where district_id = %s;
    """

    return sql


def get_district_id_by_current_member():
    sql = """
        SELECT district_id
        from member_district
        where member_id = %s;
    """

    return sql


def get_member_id_by_first_last_name():
    sql = """
        SELECT id
        FROM member
        WHERE last_name = %s AND first_name = %s 
        AND in_office = TRUE;
    """

    return sql


def get_member_id_by_last_name():
    sql = """
        SELECT id
        FROM member
        WHERE last_name = %s
        AND in_office = TRUE;
    """

    return sql


def mem_id_by_name_state():
    sql = """
        select m.id
        from member_session ms
          inner join member m on ms.member_id = m.id
          where m.last_name = %s and 
                ms.state = %s;    
        """

    return sql


def mem_id_by_name_session_state():
    sql = """
        select m.id
        from member_session ms
          inner join member m on ms.member_id = m.id
          where m.last_name = %s and 
                ms.session_num = %s and
                ms.state = %s;    
        """

    return sql


def mem_id_by_name_state_district():
    sql = """
        select m.id
        from member_session ms
          inner join member m on ms.member_id = m.id
          where m.last_name = %s and 
                ms.state = %s and
                ms.district_num= %s;
    """

    return sql


def mem_id_by_name_session_state_district():
    sql = """
        select m.id
        from member_session ms
          inner join member m on ms.member_id = m.id
          where m.last_name = %s and 
                ms.session_num = %s and
                ms.state = %s and
                ms.district_num= %s;
    """

    return sql


def get_member_id_by_state_last_name():
    sql = """
        SELECT m.id
        FROM member m
        LEFT JOIN member_session ms ON m.id = ms.member_id
        WHERE 
            ms.session_num = %s AND
            (ms.district_id ISNULL OR ms.district_id = %s) AND
            ms.state = %s AND
            m.last_name = %s;
    """

    return sql


def get_districts():
    sql = """
        SELECT id, state, district_num
        FROM district;
    """

    return sql


def get_district():
    sql = """
        SELECT id
        FROM district
        WHERE state = %s 
        AND district_num = %s;
    """
    return sql


############
# INSERTS
############

def insert_district_ids():
    sql = """
        INSERT INTO district
        (id, state, district_num)
        VALUES (DEFAULT, %s, %s)
        ON CONFLICT DO NOTHING
        RETURNING id;
    """

    return sql


def insert_member():
    sql = """
        INSERT INTO member
        (id, first_name, middle_name, last_name, suffix, birthdate, gender, in_office)
        VALUES (%s, %s, %s, %s, %s, 
                %s, %s, %s)
        ON CONFLICT DO NOTHING;                   
    """
    return sql


def insert_member_district():
    sql = """
        INSERT INTO member_district
        VALUES (%s, $s)
        ON CONFLICT DO NOTHING;
    """

    return sql


def insert_member_house():
    sql = """
        INSERT INTO member_house 
        (member_id)
        VALUES (%s)
        ON CONFLICT DO NOTHING; 
    """

    return sql


def insert_member_senate():
    sql = """
        INSERT INTO member_senate
        (member_id)  
        VALUES (%s)
        ON CONFLICT DO NOTHING;
    """

    return sql


def insert_member_session():
    sql = """
    INSERT INTO member_session
    (member_id, session_num, chamber, state, district_num, district_id, party, dw_nominate,
     total_votes, missed_votes, total_present, missed_votes_pct, votes_with_party_pct, 
     votes_against_party_pct, office_address, next_election, last_updated
)
    VALUES (%s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, 
            %s, %s) 
    ON CONFLICT (member_id, session_num)
    DO NOTHING; 
"""

    return sql


def insert_member_codes_ids():
    sql = """
        INSERT INTO member_id_url
        (member_id, govtrack_id, cspan_id, votesmart_id, icpsr_id, 
        crp_id, google_entity_id, fec_candidate_id, rss_url, url,
        youtube_id, facebook_id, twitter_id)
        VALUES (%s, %s, %s, %s, %s, 
                %s, %s, %s, %s, %s, 
                %s, %s, %s)
        ON CONFLICT DO NOTHING;                
    """

    return sql


# todo change
def insert_demographics():
    sql = """
    INSERT INTO district_summary
    (district_id, cook_pvi)
    VALUES (%s, %s)
    ON CONFLICT DO NOTHING;                     
    """

    return sql


def insert_poverty_details():
    sql = """
    INSERT INTO district_poverty_detail
    VALUES (%s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, 
            %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """

    return sql


def insert_poverty_summ():
    sql = """
    INSERT INTO district_poverty_summary
    VALUES (%s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s,             
            %s)
    ON CONFLICT DO NOTHING;
    """

    return sql


############
# UPDATES
############

def update_religion():
    sql = """
        UPDATE member
        SET religion = %s
        WHERE id = %s;
    """

    return sql


# todo
def set_member_session_district_id():
    sql = """
        UPDATE member_session
        set district_id = %s
        where state = %s 
        and district_num= %s;
    """

    return sql


def update_member_house():
    sql = """
        UPDATE member_house
        set race_2018_pct_dem = %s,
        race_2018_pct_rep = %s,
        race_2016_pct_dem = %s,
        race_2016_pct_rep = %s,
        race_2014_pct_dem = %s,
        race_2014_pct_rep = %s
        WHERE member_id = %s;
    """

    return sql


def update_member_senate():
    sql = """
            UPDATE member_senate
            set race_2018_pct_dem = %s,
            race_2018_pct_rep = %s,
            race_prior_pct_dem = %s,
            race_prior_pct_rep = %s
            WHERE member_id = %s;
        """
    return sql


def update_member():
    sql = """
            UPDATE member
            SET full_name = %s,
                race = %s,
                ethnicity = %s,
                secondary_race = %s,
                secondary_ethnicity = %s,                
                lgbtq = %s
            WHERE member_id = %s;
        """

    return sql


def update_demographics():
    sql = """
            UPDATE demographics
            SET 
                census_2010_pop_total = %s,
                census_2010_pop_white = %s,
                census_2010_pop_black = %s,
                census_2010_pop_latinx = %s,
                census_2010_pop_asian_pac = %s,
                census_2010_pop_native_amer = %s,
                census_2010_pop_other = %s,
                vote_pct_2016_clinton = %s,
                vote_pct_2016_trump = %s,
                vote_pct_2012_obama = %s,
                vote_pct_2012_romney = %s,
                vote_pct_2008_obama = %s,
                vote_pct_2008_mccain = %s
            WHERE member_id = %s;
        """

    return sql
