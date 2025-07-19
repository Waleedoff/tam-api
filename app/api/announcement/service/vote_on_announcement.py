
from sqlalchemy.orm import Session
from app.api.announcement.enums import VoteType
from app.api.announcement.models import AnnouncementVote
from app.api.auth.schema import UserResponse

def vote_on_announcement_(announcement_id: str, vote: VoteType, session: Session, current_user: UserResponse ):
    
    existing_vote = session.query(AnnouncementVote).filter_by(user_id=current_user.id, announcement_id=announcement_id).first()

    if existing_vote:
        existing_vote.vote_type = vote.value  # update the vote
    else:
        db_vote = AnnouncementVote(
            user_id=current_user.id,
            announcement_id=announcement_id,
            vote_type=vote.value,
            created_by=current_user.id
        )
        session.add(db_vote)

    session.commit()
    return {"msg": "Vote recorded."}