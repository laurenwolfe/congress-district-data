def create_district():
    sql = """
            create table district
        (
      id                serial PRIMARY KEY,
          state         varchar(2) NOT NULL,
          district_num  int        NOT NULL,
          unique (state, district_num)
        );
    """

    return sql


def create_alter_district():
    sql = """
        ALTER SEQUENCE district_id_seq RESTART WITH 100;

    """

    return sql


def create_member():
    sql = """
        create table member
        (
        id                  varchar(7) PRIMARY KEY,
        in_office           bool,
        first_name          varchar(25),
        middle_name         varchar(25),
        last_name           varchar(25),
        suffix              varchar(10),
        full_name           varchar(80),
        birthdate           date,
        gender              varchar(1),
        religion            varchar(100),
        race                varchar(20),
        secondary_race      varchar(20),
        ethnicity           varchar(50),
        secondary_ethnicity varchar(20),
        lgbtq               varchar(10)
        );
    """

    return sql


def create_member_district():
    sql = """
        create table member_district
        (
        member_id   varchar(7),
        district_id int,
        unique (member_id, district_id),
        constraint m_district_member_id_fk
        foreign key (member_id)
          references member (id),
        constraint m_district_district_id_fk
        foreign key (district_id)
          references district (id)
        );

    """

    return sql


def create_member_house():
    sql = """
        create table member_house
        (
        member_id         varchar(7) primary key,
        race_2018_pct_dem numeric,
        race_2018_pct_rep numeric,
        race_2016_pct_dem numeric,
        race_2016_pct_rep numeric,
        race_2014_pct_dem numeric,
        race_2014_pct_rep numeric,
        constraint m_house_member_id_fk
        foreign key (member_id)
          references member (id)
        );
    """

    return sql


def create_member_senate():
    sql = """
        create table member_senate
        (
        member_id          varchar(7) primary key,
        race_2018_pct_dem  numeric,
        race_2018_pct_rep  numeric,
        race_prior_pct_dem numeric,
        race_prior_pct_rep numeric,
        constraint m_senate_member_id_fk
        foreign key (member_id)
          references member (id)
        );

    """

    return sql


def create_member_id_url():
    sql = """
        create table member_id_url
        (
        member_id        varchar(7) primary key,
        govtrack_id      varchar(20),
        cspan_id         varchar(20),
        votesmart_id     varchar(20),
        icpsr_id         varchar(20),
        crp_id           varchar(20),
        google_entity_id varchar(20),
        fec_candidate_id varchar(20),
        rss_url          varchar(200),
        url              varchar(100),
        youtube_id       varchar(50),
        facebook_id      varchar(50),
        twitter_id       varchar(25),
        constraint m_id_url_member_id_fk
        foreign key (member_id)
          references member (id)
        );

    """

    return sql


def create_member_session():
    sql = """
        create table member_session
        (
        member_id               varchar(7) primary key,
        session_num             int,
        chamber                 varchar(6),
        state                   varchar(2),
        district_num            int,
        district_id             int,
        party                   varchar(1),
        dw_nominate             numeric,
        total_votes             int,
        missed_votes            int,
        total_present           int,
        missed_votes_pct        varchar(10),
        votes_with_party_pct    numeric,
        votes_against_party_pct numeric,
        office_address          varchar(100),
        next_election           int,
        last_updated            time(6),
        unique (member_id, session_num),
        constraint m_session_member_id_fk
        foreign key (member_id) references member (id)
        );

    """

    return sql


def create_district_summary():
    sql = """
        create table district_summary
        (
        district_id                 int primary key,
        cook_pvi                    varchar(6),
        census_2010_pop_total       int,
        census_2010_pop_white       int,
        census_2010_pop_black       int,
        census_2010_pop_latinx      int,
        census_2010_pop_asian_pac   int,
        census_2010_pop_native_amer int,
        census_2010_pop_other       int,
        vote_pct_2016_clinton       numeric,
        vote_pct_2016_trump         numeric,
        vote_pct_2012_obama         numeric,
        vote_pct_2012_romney        numeric,
        vote_pct_2008_obama         numeric,
        vote_pct_2008_mccain        numeric,
        constraint d_summary_district_id_fk
        foreign key (district_id) references district (id)
        );
    """

    return sql


def create_district_poverty_summary():
    sql = """
        create table district_poverty_summary
        (
        district_id         int,
        report_year         int,
        total               int,
        total_below_50_pct  int,
        total_below_125_pct int,
        total_below_150_pct int,
        total_below_185_pct int,
        total_below_200_pct int,
        total_below_300_pct int,
        total_below_400_pct int,
        total_below_500_pct int,
        unique (district_id, report_year),
        constraint d_pov_summary_district_id_fk
        foreign key (district_id) references district (id)
        );

    """

    return sql


def create_district_poverty_detail():
    sql = """
        create table district_poverty_detail
        (
        district_id       int,
        report_year       int,
        poverty_row       bool,
        total             int,
        under_18          int,
        aged_18_64        int,
        aged_over_65      int,
        male              int,
        female            int,
        white             int,
        black             int,
        native_amer_ak    int,
        asian             int,
        native_hi_pac     int,
        other             int,
        multiracial       int,
        latinx            int,
        not_hs_grad       int,
        hs_or_ged         int,
        college_to_assoc  int,
        bachelors_plus    int,
        employed_male     int,
        employed_female   int,
        unemployed_male   int,
        unemployed_female int,
        worked_full_all   int,
        worked_part       int,
        did_not_work      int,
        unique (district_id, report_year),
        constraint d_pov_detail_district_id_fk
        foreign key (district_id)
          references district (id)
        );
    """

    return sql


def create_house_expenditure():
    sql = """
            create table house_expenditure
        (
        id                 bigserial not null primary key,
        member_id          varchar(7),
        fiscal_quarter     varchar(6),
        program_category   varchar(50),
        subcategory        varchar(50),
        sort_sequence      varchar(10),
        expense_date       date,
        transcode          varchar(5),
        record_id          varchar(25),
        payee              varchar(100),
        start_date         date,
        end_date           date,
        purpose            varchar(150),
        fiscal_year        varchar(4),
        amount             numeric,
        original_recipient varchar(100),
        transcode_long     varchar(200),
        old_payee          varchar(100),
        constraint h_expenditure_member_id_fk
        foreign key (member_id)
          references member (id)
        );
"""

    return sql
