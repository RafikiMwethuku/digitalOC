def add_success_column(NFLVersePandaDataFrame):
    '''
    Adds success boolean column to a filtered NFL Verse pandas dataframe.

    success logic based on downs:
    1st down: 40% of yards needed for 1st down = success
    2nd down: 60% of yards needed for 1st down = success
    3rd/4th down: 100% of yards needed for 1st down = success

    automatic successes: gain 1st down, touchdown
    automatic failures: turnover

    @param NFLVersePandaDataFrame a pandas dataframe including info from pbp data from nfl verse
    @return the same dataframe but with an extra "success" column full of success booleans
    '''

    down = NFLVersePandaDataFrame["down"]
    ytg = NFLVersePandaDataFrame["ydstogo"]
    yg = NFLVersePandaDataFrame["yards_gained"]

    down_1 = (down == 1) & (yg >= 0.40 * ytg)
    down_2 = (down == 2) & (yg >= 0.60 * ytg)
    down_34 = ((down == 3) |  (down == 4)) & (yg >= ytg)

    auto_success = (NFLVersePandaDataFrame["first_down"] == 1) | (NFLVersePandaDataFrame["touchdown"] == 1)
    auto_failure = (
        (NFLVersePandaDataFrame['interception'] == 1) | (NFLVersePandaDataFrame["fumble_lost"] == 1)
        | (NFLVersePandaDataFrame["safety"] == 1) | (NFLVersePandaDataFrame["fourth_down_failed"] == 1)
    )

    NFLVersePandaDataFrame["new_success"] = (down_1 | down_2 | down_34 | auto_success) & (~auto_failure)

    return NFLVersePandaDataFrame


