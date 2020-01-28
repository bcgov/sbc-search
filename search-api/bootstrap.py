
from models import Corporation, CorpParty, db



c = Corporation(
  CORP_NUM="1234567890"
)

db.session.add(c)

db.session.commit()
