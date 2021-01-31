import pandas as pd


BANK_DATA_PATH = './asnlib/publicdata/bank_prepared.csv'
X_TRAIN_PATH = './asnlib/publicdata/X_train.csv'
X_TEST_PATH = './asnlib/publicdata/X_test.csv'
X_TRAIN_PREP_PATH = './asnlib/publicdata/X_train_dummies.csv'
X_TEST_PREP_PATH = './asnlib/publicdata/X_test_dummies.csv'
Y_TRAIN_PATH = './asnlib/publicdata/y_train.csv'
Y_TRAIN_PREP_PATH = './asnlib/publicdata/y_train_prep.csv'
Y_TEST_PATH = './asnlib/publicdata/y_test.csv'
Y_TEST_PREP_PATH = './asnlib/publicdata/y_test_prep.csv'


def read_training_data(final=False):
    if final:
        return pd.read_csv(X_TRAIN_PREP_PATH, index_col='index').rename_axis(None)
    else:
        return pd.read_csv(X_TRAIN_PATH, index_col='index').rename_axis(None)


def read_testing_data(final=False):
    if final:
        return pd.read_csv(X_TEST_PREP_PATH, index_col='index').rename_axis(None)
    else:
        return pd.read_csv(X_TEST_PATH, index_col='index').rename_axis(None)


def read_y_train(final=False):
    if final:
        return pd.read_csv(Y_TRAIN_PREP_PATH, index_col='index', squeeze=True).rename_axis(None)
    else:
        return pd.read_csv(Y_TRAIN_PATH, index_col='index', squeeze=True).rename_axis(None)


def read_y_test(final=False):
    if final:
        return pd.read_csv(Y_TEST_PREP_PATH, index_col='index', squeeze=True).rename_axis(None)
    else:
        return pd.read_csv(Y_TEST_PATH, index_col='index', squeeze=True).rename_axis(None)


def bin_ages(num):
        '''
        Parameters:
        num -- int or float; a number representing

        Returns: str; bin label categorizing an individual's age

        Example:

        >>> age = 31
        >>> age_binner(age)
        'thirties'

        '''
        ### BEGIN SOLUTION
        if num < 20:
            return 'teen'
        elif num < 30:
            return 'twenties'
        elif num < 40:
            return 'thirties'
        elif num < 50:
            return 'forties'
        elif num < 60:
            return 'fifties'
        else:
            return 'over sixty'


def partial(binner=bin_ages):

    X_TRAIN_PATH = './asnlib/publicdata/X_train.csv'
    X_TRAIN_PREP_PATH = './asnlib/publicdata/X_train_dummies.csv'
    COLS_TO_DROP = ['age', 'day_of_month', 'last_contact_duration',]


    def read_training_data(final=False):
        if final:
            return pd.read_csv(
                        X_TRAIN_PREP_PATH,
                        index_col='index').rename_axis(None)
        else:
            return pd.read_csv(
                        X_TRAIN_PATH,
                        index_col='index').rename_axis(None)

    df = read_training_data()
    df = df.fillna(df.median())
    df['age_binned'] = df['age'].apply(binner)
    df = df.drop(COLS_TO_DROP, axis=1)

    return df


def read_beatles():
    HEADER = ['title', 'year', 'album', 'songwriter',]
    beats = pd.read_csv(
        './asnlib/publicdata/songs.tsv',
        delimiter='\t',
        header=None,
        usecols=[0,1,2,3],
        names=HEADER
    )
    beats = beats.dropna()

    beats['to_drop'] = beats['album'].apply(lambda x: False if x[0:3] == 'UK:' else True)
    beats = beats[beats['to_drop']]
    beats = beats.drop('to_drop', axis=1)
    to_drop_albs = beats['album'].value_counts()[beats['album'].value_counts() <= 2].index.tolist()
    beats['to_drop'] = beats['album'].isin(to_drop_albs)
    beats = beats[~beats['to_drop']]
    beats = beats.drop('to_drop', axis=1)

    beatles_dict = dict()
    members = ['Lennon','McCartney','Harrison', 'Starkey']
    for idx in beats.index:
        alb = beats.loc[idx,'album']
        if not beatles_dict.get(alb):  # check if album already in there
            # set up album dictionary
            inner_dict = {m:list() for m in members}
            beatles_dict.update({alb: inner_dict})
        title = beats.loc[idx, 'title']
        writer = beats.loc[idx, 'songwriter']
        for member in members:
            if member in writer:
                beatles_dict[alb][member].append(title)
    # beatles_dict = pd.read_csv(
    #     './datasets/beatles.csv',
    #     index_col='album'
    #     ).to_dict(orient='index')
    beatles_dict = {key:[beatles_dict[key]] for key in beatles_dict}
    return beatles_dict
