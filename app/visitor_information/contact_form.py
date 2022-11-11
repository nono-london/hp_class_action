from datetime import datetime

from app.visitor_information.csv_handler import write_csv_file


def save_contact_message(form_request):
    visitor_name = form_request.get('name')
    visitor_email = form_request.get('email')
    visitor_message = form_request.get('message')
    message_datetime = datetime.utcnow().strftime("%Y-%m-%d %H-%M")
    headers = ["message_datetime", "visitor_name", "visitor_email", "visitor_message"]
    row = {"message_datetime": message_datetime, "visitor_name": visitor_name,
           "visitor_email": visitor_email, "visitor_message": visitor_message}
    write_csv_file(csv_file_name="visitor_messages.csv",
                   headers=headers, ip_address_dict=row)


if __name__ == '__main__':
    pass
