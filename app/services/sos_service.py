from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import SOSReport
from app.schemas.sos import SOSReportCreate

class SOSService:
    def get_user_sos_reports(self, db: Session, clerk_user_id: str) -> List[Dict]:
        reports = db.query(SOSReport).filter(SOSReport.clerk_user_id == clerk_user_id).all()
        return [{c.name: getattr(report, c.name) for c in report.__table__.columns} for report in reports]

    def trigger_sos(self, db: Session, sos_data: SOSReportCreate, clerk_user_id: str):
        try:
            db_sos = SOSReport(
                clerk_user_id=clerk_user_id,
                location_address=sos_data.location_address,
                latitude=sos_data.latitude,
                longitude=sos_data.longitude,
                incident_type=sos_data.incident_type,
                description=sos_data.description
            )
            db.add(db_sos)
            db.commit()
            db.refresh(db_sos)
            
            # Log the receipt of SOS signal
            print(f"SOS Triggered by {clerk_user_id} at {db_sos.timestamp}")
            
            return db_sos
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Failed to save SOS report: {str(e)}")
