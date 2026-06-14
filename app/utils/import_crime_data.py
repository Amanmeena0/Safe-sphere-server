import csv
import os
from sqlalchemy.orm import Session
from app.models.database import SessionLocal
from app.models.models import CrimeData

def import_crime_data(file_path: str):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    db: Session = SessionLocal()
    try:
        with open(file_path, mode='r', encoding='utf-8') as f:
            # Use DictReader to map columns by header name
            reader = csv.DictReader(f)
            
            # Map CSV headers to model fields
            # The CSV has some empty headers or headers that might not match exactly.
            # We'll map the core fields defined in the model.
            
            crimes_to_import = []
            count = 0
            for row in reader:
                try:
                    crime = CrimeData(
                        state_ut=row.get('state_ut'),
                        district=row.get('district'),
                        year=int(row.get('year')) if row.get('year') else None,
                        murder=int(row.get('murder')) if row.get('murder') else 0,
                        attempt_to_murder=int(row.get('attempt_to_murder')) if row.get('attempt_to_murder') else 0,
                        culpable_homicide_not_amounting_to_murder=int(row.get('culpable_homicide_not_amounting_to_murder')) if row.get('culpable_homicide_not_amounting_to_murder') else 0,
                        rape=int(row.get('rape')) if row.get('rape') else 0,
                        custodial_rape=int(row.get('custodial_rape')) if row.get('custodial_rape') else 0,
                        other_rape=int(row.get('other_rape')) if row.get('other_rape') else 0,
                        kidnapping_abduction=int(row.get('kidnapping_abduction')) if row.get('kidnapping_abduction') else 0,
                        kidnapping_and_abduction_of_women_and_girls=int(row.get('kidnapping_and_abduction_of_women_and_girls')) if row.get('kidnapping_and_abduction_of_women_and_girls') else 0,
                        kidnapping_and_abduction_of_others=int(row.get('kidnapping_and_abduction_of_others')) if row.get('kidnapping_and_abduction_of_others') else 0,
                        dacoity=int(row.get('dacoity')) if row.get('dacoity') else 0,
                        preparation_and_assembly_for_dacoity=int(row.get('preparation_and_assembly_for_dacoity')) if row.get('preparation_and_assembly_for_dacoity') else 0,
                        robbery=int(row.get('robbery')) if row.get('robbery') else 0,
                        burglary=int(row.get('burglary')) if row.get('burglary') else 0,
                        theft=int(row.get('theft')) if row.get('theft') else 0,
                        auto_theft=int(row.get('auto_theft')) if row.get('auto_theft') else 0,
                        other_theft=int(row.get('other_theft')) if row.get('other_theft') else 0,
                        riots=int(row.get('riots')) if row.get('riots') else 0,
                        criminal_breach_of_trust=int(row.get('criminal_breach_of_trust')) if row.get('criminal_breach_of_trust') else 0,
                        cheating=int(row.get('cheating')) if row.get('cheating') else 0,
                        counterfeiting=int(row.get('counterfeiting')) if row.get('counterfeiting') else 0,
                        arson=int(row.get('arson')) if row.get('arson') else 0,
                        hurt_grevious_hurt=int(row.get('hurt_grevious_hurt')) if row.get('hurt_grevious_hurt') else 0,
                        dowry_deaths=int(row.get('dowry_deaths')) if row.get('dowry_deaths') else 0,
                        assault_on_women_with_intent_to_outrage_her_modesty=int(row.get('assault_on_women_with_intent_to_outrage_her_modesty')) if row.get('assault_on_women_with_intent_to_outrage_her_modesty') else 0,
                        insult_to_modesty_of_women=int(row.get('insult_to_modesty_of_women')) if row.get('insult_to_modesty_of_women') else 0,
                        cruelty_by_husband_or_his_relatives=int(row.get('cruelty_by_husband_or_his_relatives')) if row.get('cruelty_by_husband_or_his_relatives') else 0,
                        importation_of_girls_from_foreign_countries=int(row.get('importation_of_girls_from_foreign_countries')) if row.get('importation_of_girls_from_foreign_countries') else 0,
                        causing_death_by_negligence=int(row.get('causing_death_by_negligence')) if row.get('causing_death_by_negligence') else 0,
                        other_ipc_crimes=int(row.get('other_ipc_crimes')) if row.get('other_ipc_crimes') else 0,
                        total_ipc_crimes=int(row.get('total_ipc_crimes')) if row.get('total_ipc_crimes') else 0
                    )
                    crimes_to_import.append(crime)
                    count += 1
                    
                    # Batch commit every 1000 rows
                    if count % 1000 == 0:
                        db.bulk_save_objects(crimes_to_import)
                        db.commit()
                        crimes_to_import = []
                        print(f"Imported {count} rows...")
                except Exception as e:
                    print(f"Skipping row due to error: {e}")
            
            # Final commit for remaining rows
            if crimes_to_import:
                db.bulk_save_objects(crimes_to_import)
                db.commit()
            
            print(f"Successfully imported {count} records into the crime_data table.")
            
    except Exception as e:
        db.rollback()
        print(f"Failed to import data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    # Get the project root directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    csv_path = os.path.join(project_root, "store", "crime_data.csv")
    import_crime_data(csv_path)
