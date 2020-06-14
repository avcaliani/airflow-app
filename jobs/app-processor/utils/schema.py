import pyarrow


def jokes():
    return pyarrow.schema([
        ('id'          , pyarrow.string()),
        ('value'       , pyarrow.string()),
        ('icon_url'    , pyarrow.string()),
        ('url'         , pyarrow.string()),
        ('created_at'  , pyarrow.timestamp('s')),
        ('updated_at'  , pyarrow.timestamp('s')),
        ('persisted_at', pyarrow.timestamp('s'))
    ])
