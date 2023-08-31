from flask_mail import Message, Mail
from flask import render_template
from utilities.generate_doc import generate_doc
import io

mail = Mail()

def send_mail(user_data):
    studio_name = user_data['studio_name']
    email = user_data['email']
    contact_number = user_data['contact_number']
    couple_name = user_data['couple_name']
    wedding_date = user_data['wedding_date']
    source_link = user_data['source_link']
    file_size = user_data['file_size']
    highlight = user_data['highlight']
    music_option = ", ".join(user_data['music_option'])
    order_date = user_data['order_date']
    description = user_data['description']

    file_name = couple_name.replace(" ", '-') + '.xlsx'
    table_data = [
        ['studio_name', 'email', 'contact_number', 'couple_name', 'wedding_date', 
        'source_link', 'file_size', 'highlight', 'music_option', 'order_date', 'description'],
        [studio_name, email, contact_number, couple_name, wedding_date, source_link,
         file_size, highlight, music_option, order_date, description]
    ]
    workbook = generate_doc(table_data)

    # Convert .xlsx content to bytes
    xlsx_stream = io.BytesIO()
    workbook.save(xlsx_stream)
    xlsx_stream.seek(0)


    msg = Message(
                sender ='edit0r2ise@gmail.com',
                recipients = ['edit0r2ise@gmail.com']
               )
    msg.subject = 'New customer'
    msg.html = render_template('email_template.html', studio_name=studio_name,
                               email=email, contact_number=contact_number,
                               couple_name=couple_name, wedding_date=wedding_date,
                               source_link=source_link,file_size=file_size,
                               highlight=highlight,music_option=music_option,
                               order_date=order_date,description=description)
    msg.attach(filename=file_name, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', data=xlsx_stream.read())
                                
    mail.send(msg)