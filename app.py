from flask import Flask, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/process_excel', methods=['POST'])
def process_excel():
    # Retrieve the file from the request
    file = request.files['file']
    
    # Read the file into a pandas dataframe
    df = pd.read_excel(file)
    
    # Add the 'username' column to the dataframe
    df['username'] = df['email']
    
    # Split the 'username' column into 'firstname' and 'lastname' columns
    df[['firstname', 'lastname']] = df['username'].str.split('.', expand=True)
    
    # Capitalize the first letter of 'firstname' and 'lastname'
    df['firstname'] = df['firstname'].str.capitalize()
    df['lastname'] = df['lastname'].str.capitalize()
    
    # Add the 'alias' column to the dataframe
    df['alias'] = df['firstname'].str[0] + df['lastname'].str[:4]
    
    # Save the processed dataframe to a BytesIO buffer
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    
    # Return the processed file as a response
    return send_file(
        buffer,
        as_attachment=True,
        attachment_filename='email_with_username_firstname_lastname_alias.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)
