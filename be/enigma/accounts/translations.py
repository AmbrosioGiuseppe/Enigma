from settings.models import AllSetting

allSettings = AllSetting.load()

translations = {
    'ENGLISH': {
        "subject_verification_email": "E-mail Verification"
    },
    'ITALIAN': {
        "subject_verification_email": "Verifica E-mail"
    },
}