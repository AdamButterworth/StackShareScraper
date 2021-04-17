# Define a min threshold for features below which companies are ignored
MINIMUM_THRESHOLD = 10
# Daily growth rate deemed interesting - 1%
DOD_GROWTH_RATE = 0.01
# Weekly growth rate deemed interesting - 5%
WOW_GROWTH_RATE = 0.05
# Weekly growth rate deemed interesting - 10%
MOM_GROWTH_RATE = 0.1

FEATURE_SET_DIFF = ["num_companies", "num_developers",
                    "num_integrations", "num_followers"]


def find_interesting_companies(df):
    '''Pass in a dataframe into this function
to identify interesting companies'''

    interesting_companies = set()
    company_names = list(df.name.unique())

    for company in company_names:
        if is_interesting_company(company, df):
            interesting_companies.add(company)

    return interesting_companies


def is_interesting_company(company, df):
    return company_has_strong_growth(company, df) or company_is_strong_vs_competitors(company, df)


def company_has_strong_growth(company, df):
    # Evaluate whether company has strong growth
    company_df = df[df['name'] == company]
    # Sort by descending date
    company_df.sort_values(by=['date'], ascending=False)
    # Get difference in sequential rows to get DoD growth
    for feature in FEATURE_SET_DIFF:
        # Get difference in sequential rows to get DoD growth
        company_df[str(feature + '_growth_dod')
                   ] = company_df[feature].pct_change(-1)
        # Get difference in weekly rows to get WoW growth
        company_df[str(feature + '_growth_wow')
                   ] = company_df[feature].pct_change(-7)
        # Get difference in weekly rows to get MoM growth
        company_df[str(feature + '_growth_mom')
                   ] = company_df[feature].pct_change(-7)
        # If growth rate exceeds our predetermined value, return true, else false
        # For the moment, we only return those with a strong growth rate for the most recent day
        if company_df[str(feature + '_growth_dod')].iloc[0] > DOD_GROWTH_RATE or \
                company_df[str(feature + '_growth_wow')].iloc[0] > WOW_GROWTH_RATE or \
                company_df[str(feature + '_growth_mom')].iloc[0] > MOM_GROWTH_RATE:
            return True

    return False


def company_is_strong_vs_competitors(company, df):
    pass
