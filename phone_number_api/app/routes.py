from flask import Blueprint, request, jsonify
import phonenumbers

app = Blueprint('routes', __name__)

@app.route('/validate-phone', methods=['POST'])
def validate_phone():
    data = request.get_json()
    phone_number = data.get('phone_number')

    if not phone_number:
        return jsonify({"error": "Phone number is required"}), 400

    # Verificar si el número de teléfono comienza con un prefijo internacional (+)
    if not phone_number.startswith('+'):
        return jsonify({"error": "Please include the country prefix in the phone number."}), 400

    try:
        # Parse el número con el prefijo internacional
        parsed_number = phonenumbers.parse(phone_number)
        is_valid = phonenumbers.is_valid_number(parsed_number)

        if is_valid:
            return jsonify({
                "valid": True,
                "international_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                "national_format": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                "country_code": parsed_number.country_code
            })
        else:
            return jsonify({"valid": False, "error": "Invalid phone number format"}), 400
    except phonenumbers.NumberParseException as e:
        return jsonify({"valid": False, "error": str(e)}), 400