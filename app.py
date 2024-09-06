# import streamlit as st
# import sqlite3
# from openai import OpenAI
# from streamlit_sortables import sort_items
# import re
# import os

# # Set your OpenAI API key
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
# client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# # Database connection function
# def get_db_connection():
#     conn = sqlite3.connect('product_descriptions.db')
#     conn.row_factory = sqlite3.Row
#     return conn

# # Function to insert product into the database
# def insert_product(product_name):
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute('INSERT INTO products (name) VALUES (?)', (product_name,))
#     conn.commit()
#     product_id = cursor.lastrowid  # Get the last inserted product ID
#     conn.close()
#     return product_id

# # Function to delete product from the database
# def delete_product(product_id):
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Delete product and associated descriptions
#     cursor.execute('DELETE FROM descriptions WHERE product_id = ?', (product_id,))
#     cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
#     conn.commit()
#     conn.close()

# # Initialize session state for page control
# if "current_page" not in st.session_state:
#     st.session_state.current_page = "Page 1"

# if st.session_state.current_page == "Page 1":
#     st.title("Product Description Generator")

#     # Step 1: Prompt user to enter a product name
#     product_name = st.text_input("Enter the product name:")

#     # Handle the logic only when a product name is provided and not yet saved
#     if product_name:
#         # Check if a product has already been added in this session
#         if "product_id" not in st.session_state:
#             # Insert the product name into the database and store the product_id in session state
#             product_id = insert_product(product_name)
#             st.session_state["product_id"] = product_id
#             st.session_state["product_name"] = product_name
#         else:
#             product_id = st.session_state["product_id"]
#         # Check if a description has already been generated in this session
#         if "generated_description" not in st.session_state and product_id:
#             # Create the OpenAI prompt
#             openai_prompt = f"""
#             You are working with a Kirana store owner to generate a good product description for {product_name}. 
#             Create two different lists of Unique Selling Propositions. First, there should be a generic list of Unique Selling Propositions that apply to all {product_name}. 
#             Second, there should be a specific list of Unique Selling Propositions that are based on attributes specific only to certain types of {product_name}. 
#             The header of each item on both list should be followed by *. The format should be "Header*: Detail". Be sure not to include any item in the second list that would apply to all {product_name}. 
#             Make sure there are not more than 6 items in each of the lists. For both lists, include bolded headers for each item, but do not include the product name {product_name} in any of the headers. 
#             Number the lists in a continuous sequence. For both the lists, mention only the items in the list without a title for the lists.
#             """

#             # Step 3: Call the OpenAI API to generate the description
#             with st.spinner("Generating product attributes..."):
#                 completion = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
#                         {"role": "user", "content": openai_prompt}
#                     ]
#                 )

#                 # Extract the generated text and store it in session state
#                 generated_description = completion.choices[0].message.content
#                 st.session_state["generated_description"] = generated_description
#         else:
#             generated_description = st.session_state["generated_description"]

#         # Process the generated description
#         description_lines = []
#         for line in generated_description.split('\n'):
#             if line.strip():
#                 # Remove numbers and whitespace from the beginning of the line
#                 line = re.sub(r"^\d+\.\s*", "", line.strip())
#                 print(line)
#                 # Split the line at the first colon (:) to separate the title and description
#                 if ": " in line:
#                     title, description = line.split(": ", 1)

#                     # Check if the title contains an asterisk (*) and handle accordingly
#                     if "*" in title:
#                         # Move the asterisk after the title without separating with a colon
#                         title = title.replace("*", "") + "*"
#                         bold_title=title.upper()
                    
#                     # Format the final string using f-strings
#                     formatted_line = f"{bold_title}: {description}"
#                     description_lines.append(formatted_line)
#                 else:
#                     # If no colon is found, add the line as is
#                     description_lines.append(line)


#         # Display the generated product description as selectable items
#         st.subheader("Select up to 6 Attributes:")
#         selected_attributes = st.multiselect(
#             "Choose attributes:",
#             description_lines,
#             max_selections=6
#         )

#         # Count selected attributes
#         selected_count = len(selected_attributes)

#         # Custom description input
#         st.subheader("Add Custom Descriptions:")

#         # Separate inputs for title and description
#         custom_title = st.text_input("Enter a custom title:")
#         custom_description = st.text_area("Enter a custom description:")

#         # Check how many custom descriptions have been added in session state
#         custom_descriptions = st.session_state.get("custom_descriptions", [])
#         custom_count = len(custom_descriptions)

#         # Total attributes selected (generated + custom)
#         total_selected = selected_count + custom_count

#         if total_selected >= 6:
#             st.warning("You have reached the limit of 6 attributes. No more attributes can be added.")
#         else:
#             if st.button("Add Custom Description"):
#                 if custom_title and custom_description:
#                     # Ensure the user can add custom attributes only if total count is less than 6
#                     if total_selected < 6:
#                         if "custom_descriptions" not in st.session_state:
#                             st.session_state["custom_descriptions"] = []
                        
#                         # Combine title and description into one line (formatted as needed)
#                         custom_combined = f"{custom_title.upper()}*: {custom_description}"

#                         # Add combined custom description
#                         st.session_state["custom_descriptions"].append(custom_combined)
#                         st.success(f"Custom description added! Total selected: {total_selected + 1}")
#                     else:
#                         st.warning("You can only add up to 6 attributes.")
#                 else:
#                     st.warning("Please enter both a title and a description to add.")

#         # Show the number of remaining attributes the user can add
#         remaining_attributes = 6 - total_selected



#         # Layout with two columns for buttons
#         col1, col2 = st.columns([8, 2])  # Adjust column widths as needed

#         with col1:
#             # If attributes are selected, navigate to Page 2
#             if st.button("Save Selected Attributes"):
#                 if selected_attributes or "custom_descriptions" in st.session_state and st.session_state["custom_descriptions"]:
#                     st.session_state["selected_attributes"] = selected_attributes
#                     st.session_state.current_page = "Page 2"
#                     st.rerun()
#                 else:
#                     st.warning("Please select at least one attribute or add a custom description.")

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()

# if st.session_state.current_page == "Page 2":
#     st.title("Set Priorities for Selected Attributes")

#     if "selected_attributes" in st.session_state:
#         selected_attributes = st.session_state["selected_attributes"]

#         custom_descriptions = st.session_state.get("custom_descriptions", [])
#         all_descriptions = selected_attributes + custom_descriptions

#         sortable_key = "sortable_descriptions_" + str(st.session_state.get("product_id", 0))

#         st.subheader("Set Priority for Each Description:")
#         st.write("Drag and drop to reorder descriptions:")
#         sorted_descriptions = sort_items(all_descriptions, key=sortable_key)

#         # Layout with two columns for buttons
#         col1, col2 = st.columns([8, 2])  # Adjust column widths as needed

#         with col1:
#             if st.button("Save Priorities to Database"):
#                 product_id = st.session_state.get("product_id")
#                 if product_id:
#                     conn = get_db_connection()
#                     cursor = conn.cursor()
#                     cursor.execute('DELETE FROM attributes WHERE product_id = ?', (product_id,))
#                     for idx, description in enumerate(sorted_descriptions, start=1):
#                         cursor.execute('''
#                             INSERT INTO attributes (product_id, attribute, priority)
#                             VALUES (?, ?, ?)
#                         ''', (product_id, description, idx))
#                     conn.commit()
#                     conn.close()
#                     st.success("Priorities have been saved to the database!")
#                     # st.rerun()

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()

#         if st.button("Continue"):
#             st.session_state.current_page = "Page 3"
#             st.rerun()
#     else:
#         st.error("No attributes found. Please go back to Page 1 and select attributes.")





# elif st.session_state.current_page == "Page 3":
#     st.title("Long Product Description")

#     product_id = st.session_state.get("product_id")
#     if product_id:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Fetch product name
#         cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
#         product_name_row = cursor.fetchone()
#         if product_name_row:
#             product_name = product_name_row['name']
#             st.session_state["product_name"] = product_name
#         else:
#             st.error("Product name not found in the database.")
#             st.stop()

#         # Fetch attributes
#         cursor.execute('SELECT attribute FROM attributes WHERE product_id = ? ORDER BY priority', (product_id,))
#         attributes = cursor.fetchall()
#         selected_attributes = [row['attribute'] for row in attributes]
#         st.session_state["selected_attributes"] = selected_attributes

#         conn.close()

#         if "long_description" not in st.session_state:
#             openai_prompt = f"""
#             Generate a product description with the USPs mentioned. Start with a paragraph of information which is firstly, not same as the USPs,and secondly, not more than 60 words from the following : the problem the product solves for the customer, where and when is the customer going to use the product, how is the product better than other products in the market for the buyer? How does the product work to solve the problem of the buyers? Then, add the USPs mentioned, but do not use the term USPs and make each USP title appear in bold. Do not change the description of the USPs. Use Simple language understood by a grade 5 student) but retains important terms or keywords about the {product_name} product.
#             {chr(10).join(selected_attributes)}
#             """

#             with st.spinner("Generating long product description..."):
#                 completion = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
#                         {"role": "user", "content": openai_prompt}
#                     ]
#                 )

#                 long_description = completion.choices[0].message.content
#                 st.session_state["long_description"] = long_description

#         long_description = st.session_state["long_description"]

#         st.subheader("Long Product Description:")

#         # Check if the user is in "edit mode"
#         if "edit_mode" not in st.session_state:
#             st.session_state["edit_mode"] = False

#         if st.session_state["edit_mode"]:
#             # Show text box for editing the description
#             long_description = st.text_area("Edit Description:", value=long_description, height=300)

#             if st.button("Save Edited Description"):
#                 st.session_state["long_description"] = long_description
#                 st.session_state["edit_mode"] = False
#                 st.success("Description updated!")
#                 st.rerun()
#         else:
#             # Show description as markdown
#             st.markdown(st.session_state["long_description"])

#             if st.button("Edit"):
#                 st.session_state["edit_mode"] = True
#                 st.rerun()

#         if st.button("Save Long Description"):
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 REPLACE INTO descriptions (product_id, long_description)
#                 VALUES (?, ?)
#             ''', (product_id, long_description))
#             conn.commit()
#             conn.close()
#             st.success("Long description saved!")
#             # st.rerun()

#         # Layout with two columns for buttons
#         col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


#         with col1:
#             # Continue to Page 4
#             if st.button("Continue"):
#                 st.session_state.current_page = "Page 4"
#                 st.rerun()

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()

        
#     else:
#         st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")







# elif st.session_state.current_page == "Page 4":
#     st.title("Short Product Description-Bullets")

#     product_id = st.session_state.get("product_id")
#     if product_id:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Fetch product name
#         cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
#         product_name_row = cursor.fetchone()
#         if product_name_row:
#             product_name = product_name_row['name']
#             st.session_state["product_name"] = product_name
#         else:
#             st.error("Product name not found in the database.")
#             st.stop()

#         # Fetch long product description
#         cursor.execute('SELECT long_description FROM descriptions WHERE product_id = ?', (product_id,))
#         long_description_row = cursor.fetchone()
#         if long_description_row:
#             long_description = long_description_row['long_description']
#             st.session_state["long_description"] = long_description
#         else:
#             st.error("Long description not found in the database.")
#             st.stop()

#         conn.close()

#         if "short_description_bullets" not in st.session_state:
#             openai_prompt = f"""
#             Create a much shorter version of the following product description in which the initial paragraph is about half as long as the original and each USP description is about half as long. Keep the USP titles as is. 
#             {long_description}
#             """

#             with st.spinner("Generating short product description..."):
#                 completion = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
#                         {"role": "user", "content": openai_prompt}
#                     ]
#                 )

#                 short_description_bullets = completion.choices[0].message.content
#                 st.session_state["short_description_bullets"] = short_description_bullets

#         short_description_bullets = st.session_state["short_description_bullets"]

#         st.subheader("Short Product Description Bullets:")

#         # Check if the user is in "edit mode"
#         if "edit_mode_bullets" not in st.session_state:
#             st.session_state["edit_mode_bullets"] = False

#         if st.session_state["edit_mode_bullets"]:
#             # Show text box for editing the description
#             short_description_bullets = st.text_area("Edit Description Bullets:", value=short_description_bullets, height=300)

#             if st.button("Save Edited Description Bullets"):
#                 st.session_state["short_description_bullets"] = short_description_bullets
#                 st.session_state["edit_mode_bullets"] = False
#                 st.success("Short description bullets updated!")
#                 st.rerun()
#         else:
#             # Show description as markdown
#             st.markdown(st.session_state["short_description_bullets"])

#             if st.button("Edit Description Bullets"):
#                 st.session_state["edit_mode_bullets"] = True
#                 st.rerun()

#         if st.button("Save Short Description Bullets"):
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 REPLACE INTO descriptions (product_id, long_description, short_description_bullets)
#                 VALUES (?, ?, ?)
#             ''', (product_id, long_description, short_description_bullets))
#             conn.commit()
#             conn.close()
#             st.success("Short description saved!")
#             # st.rerun()

#         # Layout with two columns for buttons
#         col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


#         with col1:
#             # Continue to Page 5
#             if st.button("Continue"):
#                 st.session_state.current_page = "Page 5"
#                 st.rerun()

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()

#     else:
#         st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")




# elif st.session_state.current_page == "Page 5":
#     st.title("Short Product Description-Paragraph")

#     product_id = st.session_state.get("product_id")
#     if product_id:
#         conn = get_db_connection()
#         cursor = conn.cursor()

#         # Fetch product name
#         cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
#         product_name_row = cursor.fetchone()
#         if product_name_row:
#             product_name = product_name_row['name']
#             st.session_state["product_name"] = product_name
#         else:
#             st.error("Product name not found in the database.")
#             st.stop()

#         # Fetch long product description
#         cursor.execute('SELECT long_description FROM descriptions WHERE product_id = ?', (product_id,))
#         long_description_row = cursor.fetchone()
#         if long_description_row:
#             long_description = long_description_row['long_description']
#             st.session_state["long_description"] = long_description
#         else:
#             st.error("Long description not found in the database.")
#             st.stop()

#         # Fetch short product description (bullets)
#         cursor.execute('SELECT short_description_bullets FROM descriptions WHERE product_id = ?', (product_id,))
#         short_description_row = cursor.fetchone()
#         if short_description_row:
#             short_description_bullets = short_description_row['short_description_bullets']
#             st.session_state["short_description_bullets"] = short_description_bullets
#         else:
#             st.error("Short description bullets not found in the database.")
#             st.stop()

#         conn.close()

#         if "short_description_paragraph" not in st.session_state:
#             openai_prompt = f"""
#             Rewrite the below short product description in paragraph form. Keep the USPs in bold letters in sentence case.
#             {short_description_bullets}
#             """

#             with st.spinner("Generating short product description..."):
#                 completion = client.chat.completions.create(
#                     model="gpt-4o",
#                     messages=[
#                         {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
#                         {"role": "user", "content": openai_prompt}
#                     ]
#                 )

#                 short_description_paragraph = completion.choices[0].message.content
#                 st.session_state["short_description_paragraph"] = short_description_paragraph

#         short_description_paragraph = st.session_state["short_description_paragraph"]

#         st.subheader("Short Product Description Paragraph:")

#         # Check if the user is in "edit mode"
#         if "edit_mode_paragraph" not in st.session_state:
#             st.session_state["edit_mode_paragraph"] = False

#         if st.session_state["edit_mode_paragraph"]:
#             # Show text box for editing the description paragraph
#             short_description_paragraph = st.text_area("Edit Description Paragraph:", value=short_description_paragraph, height=300)

#             if st.button("Save Edited Description Paragraph"):
#                 st.session_state["short_description_paragraph"] = short_description_paragraph
#                 st.session_state["edit_mode_paragraph"] = False
#                 st.success("Short description paragraph updated!")
#                 st.rerun()
#         else:
#             # Show description as markdown
#             st.markdown(st.session_state["short_description_paragraph"])

#             if st.button("Edit Description Paragraph"):
#                 st.session_state["edit_mode_paragraph"] = True
#                 st.rerun()

#         if st.button("Save Short Description Paragraph"):
#             conn = get_db_connection()
#             cursor = conn.cursor()
#             cursor.execute('''
#                 REPLACE INTO descriptions (product_id, long_description, short_description_bullets, short_description_paragraph)
#                 VALUES (?, ?, ?, ?)
#             ''', (product_id, long_description, short_description_bullets, short_description_paragraph))
#             conn.commit()
#             conn.close()
#             st.success("Short description saved!")

#         # Layout with two columns for buttons
#         col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


#         with col1:
#             # Continue to Page 6
#             if st.button("Continue"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()

#         with col2:
#             if st.button("Cancel"):
#                 st.session_state.current_page = "Page 6"
#                 st.rerun()


#     else:
#         st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")



# elif st.session_state.current_page == "Page 6":
#     st.title("Product Details and Descriptions")

#     conn = get_db_connection()
#     cursor = conn.cursor()

#     # Fetch all products with their details and descriptions
#     cursor.execute('''
#         SELECT p.id, p.name, d.long_description, d.short_description_bullets, d.short_description_paragraph
#         FROM products p
#         LEFT JOIN descriptions d ON p.id = d.product_id
#     ''')
#     products = cursor.fetchall()

#     if products:
#         for product in products:
#             product_id, product_name, long_description, short_description_bullets, short_description_paragraph = product

#             st.write(f"**Product Name:** {product_name}")

#             # Expandable sections for descriptions
#             with st.expander("Long Description"):
#                 st.write(long_description if long_description else "No long description available.")

#             with st.expander("Short Description (Bullets)"):
#                 st.write(short_description_bullets if short_description_bullets else "No short description (bullets) available.")

#             with st.expander("Short Description (Paragraph)"):
#                 st.write(short_description_paragraph if short_description_paragraph else "No short description (paragraph) available.")

#             # Delete button for each product
#             if st.button(f"Delete {product['name']}"):
#                 delete_product(product['id'])
#                 st.success(f"Product '{product['name']}' has been deleted.")
#                 st.rerun()  # Refresh the page to reflect the deletion
                
#             st.write("---")  # Separator between products

#     conn.close()

#     if st.button("Add New Product"):
#         if "product_id" in st.session_state:
#             del st.session_state["product_id"]
#         if "product_name" in st.session_state:
#             del st.session_state["product_name"]
#         if "selected_attributes" in st.session_state: 
#             del st.session_state["selected_attributes"]
#         if "generated_description" in st.session_state: 
#             del st.session_state["generated_description"]
#         if "long_description" in st.session_state: 
#             del st.session_state["long_description"]
#         if "short_description_bullets" in st.session_state:  
#             del st.session_state["short_description_bullets"]
#         if "short_description_paragraph" in st.session_state:  
#             del st.session_state["short_description_paragraph"]




#         st.session_state.usps = []
#         st.session_state.attributes = []
#         st.session_state.descriptions = []
#         st.session_state.attributes = []

#         st.session_state.current_page = "Page 1"
#         st.write("Redirecting to Page 1...")
#         st.rerun()






















































































import streamlit as st
import sqlite3
from openai import OpenAI
from streamlit_sortables import sort_items
import re
import os

# Set your OpenAI API key
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('product_descriptions.db')
    conn.row_factory = sqlite3.Row
    return conn

# Function to insert product into the database
def insert_product(product_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO products (name) VALUES (?)', (product_name,))
    conn.commit()
    product_id = cursor.lastrowid  # Get the last inserted product ID
    conn.close()
    return product_id

# Function to delete product from the database
def delete_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete product and associated descriptions
    cursor.execute('DELETE FROM descriptions WHERE product_id = ?', (product_id,))
    cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
    
    conn.commit()
    conn.close()

# Initialize session state for page control
if "current_page" not in st.session_state:
    st.session_state.current_page = "Page 1"

if st.session_state.current_page == "Page 1":
    st.title("Product Description Generator")

    # Step 1: Prompt user to enter a product name
    product_name = st.text_input("Enter the product name:")

    # Handle the logic only when a product name is provided and not yet saved
    if product_name:
        # Check if a product has already been added in this session
        if "product_id" not in st.session_state:
            # Insert the product name into the database and store the product_id in session state
            product_id = insert_product(product_name)
            st.session_state["product_id"] = product_id
            st.session_state["product_name"] = product_name
        else:
            product_id = st.session_state["product_id"]
        # Check if a description has already been generated in this session
        if "generated_description" not in st.session_state and product_id:
            # Create the OpenAI prompt
            openai_prompt = f"""
            You are working with a Kirana store owner to generate a good product description for {product_name}. 
            Create two different lists of Unique Selling Propositions. First, there should be a generic list of Unique Selling Propositions that apply to all {product_name}. 
            Second, there should be a specific list of Unique Selling Propositions that are based on attributes specific only to certain types of {product_name}. 
            The header of each item on both list should be followed by *. The format should be "Header*: Detail". Be sure not to include any item in the second list that would apply to all {product_name}. 
            Make sure there are not more than 6 items in each of the lists. For both lists, include bolded headers for each item, but do not include the product name {product_name} in any of the headers. 
            Number the lists in a continuous sequence. For both the lists, mention only the items in the list without a title for the lists.
            """

            # Step 3: Call the OpenAI API to generate the description
            with st.spinner("Generating product attributes..."):
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                        {"role": "user", "content": openai_prompt}
                    ]
                )

                # Extract the generated text and store it in session state
                generated_description = completion.choices[0].message.content
                st.session_state["generated_description"] = generated_description
        else:
            generated_description = st.session_state["generated_description"]

        # Process the generated description
        description_lines = []
        for line in generated_description.split('\n'):
            if line.strip():
                # Remove numbers and whitespace from the beginning of the line
                line = re.sub(r"^\d+\.\s*", "", line.strip())
                print(line)
                # Split the line at the first colon (:) to separate the title and description
                if ": " in line:
                    title, description = line.split(": ", 1)

                    # Check if the title contains an asterisk (*) and handle accordingly
                    if "*" in title:
                        # Move the asterisk after the title without separating with a colon
                        title = title.replace("*", "") + "*"
                        bold_title=title.upper()
                    
                    # Format the final string using f-strings
                    formatted_line = f"{bold_title}: {description}"
                    description_lines.append(formatted_line)
                else:
                    # If no colon is found, add the line as is
                    description_lines.append(line)


        # Display the generated product description as selectable items
        st.subheader("Select up to 6 Attributes:")
        selected_attributes = st.multiselect(
            "Choose attributes:",
            description_lines,
            max_selections=6
        )

        # Count selected attributes
        selected_count = len(selected_attributes)

        # Custom description input
        st.subheader("Add Custom Descriptions:")

        # Separate inputs for title and description
        custom_title = st.text_input("Enter a custom title:")
        custom_description = st.text_area("Enter a custom description:")

        # Check how many custom descriptions have been added in session state
        custom_descriptions = st.session_state.get("custom_descriptions", [])
        custom_count = len(custom_descriptions)

        # Total attributes selected (generated + custom)
        total_selected = selected_count + custom_count

        if total_selected >= 6:
            st.warning("You have reached the limit of 6 attributes. No more attributes can be added.")
        else:
            if st.button("Add Custom Description"):
                if custom_title and custom_description:
                    # Ensure the user can add custom attributes only if total count is less than 6
                    if total_selected < 6:
                        if "custom_descriptions" not in st.session_state:
                            st.session_state["custom_descriptions"] = []
                        
                        # Combine title and description into one line (formatted as needed)
                        custom_combined = f"{custom_title.upper()}*: {custom_description}"

                        # Add combined custom description
                        st.session_state["custom_descriptions"].append(custom_combined)
                        st.success(f"Custom description added! Total selected: {total_selected + 1}")
                    else:
                        st.warning("You can only add up to 6 attributes.")
                else:
                    st.warning("Please enter both a title and a description to add.")

        # Show the number of remaining attributes the user can add
        remaining_attributes = 6 - total_selected



        # Layout with two columns for buttons
        col1, col2 = st.columns([8, 2])  # Adjust column widths as needed

        with col1:
            # If attributes are selected, navigate to Page 2
            if st.button("Save Selected Attributes"):
                if selected_attributes or "custom_descriptions" in st.session_state and st.session_state["custom_descriptions"]:
                    st.session_state["selected_attributes"] = selected_attributes
                    st.session_state.current_page = "Page 2"
                    st.rerun()
                else:
                    st.warning("Please select at least one attribute or add a custom description.")

        with col2:
            if st.button("Cancel"):
                st.session_state.current_page = "Page 6"
                st.rerun()

if st.session_state.current_page == "Page 2":
    st.title("Set Priorities for Selected Attributes")

    if "selected_attributes" in st.session_state:
        selected_attributes = st.session_state["selected_attributes"]

        custom_descriptions = st.session_state.get("custom_descriptions", [])
        all_descriptions = selected_attributes + custom_descriptions

        sortable_key = "sortable_descriptions_" + str(st.session_state.get("product_id", 0))

        st.subheader("Set Priority for Each Description:")
        st.write("Drag and drop to reorder descriptions:")

        # Initialize sorted descriptions if they don't already exist
        if "sorted_descriptions" not in st.session_state:
            st.session_state["sorted_descriptions"] = sort_items(all_descriptions, key=sortable_key)

        sorted_descriptions = st.session_state["sorted_descriptions"]

        # Display each description with a delete button
        for idx, description in enumerate(sorted_descriptions):
            col1, col2 = st.columns([9, 1])  # Adjust column widths to fit "Delete" button
            with col1:
                st.text(description)
            with col2:
                if st.button("Delete", key=f"delete_{idx}"):
                    # Remove the description from the sorted list
                    sorted_descriptions.pop(idx)
                    st.session_state["sorted_descriptions"] = sorted_descriptions  # Update session state
                    st.rerun()  # Rerun to update the UI

        # Layout with two columns for buttons
        col1, col2 = st.columns([8, 3])  # Adjust column widths as needed

        with col1:
            if st.button("Save Priorities to Database"):
                product_id = st.session_state.get("product_id")
                if product_id:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('DELETE FROM attributes WHERE product_id = ?', (product_id,))
                    for idx, description in enumerate(sorted_descriptions, start=1):
                        cursor.execute('''
                            INSERT INTO attributes (product_id, attribute, priority)
                            VALUES (?, ?, ?)
                        ''', (product_id, description, idx))
                    conn.commit()
                    conn.close()
                    st.success("Priorities have been saved to the database!")
                    # st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.current_page = "Page 6"
                st.rerun()

        if st.button("Continue"):
            st.session_state.current_page = "Page 3"
            st.rerun()
    else:
        st.error("No attributes found. Please go back to Page 1 and select attributes.")






elif st.session_state.current_page == "Page 3":
    st.title("Long Product Description")

    product_id = st.session_state.get("product_id")
    if product_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch product name
        cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
        product_name_row = cursor.fetchone()
        if product_name_row:
            product_name = product_name_row['name']
            st.session_state["product_name"] = product_name
        else:
            st.error("Product name not found in the database.")
            st.stop()

        # Fetch attributes
        cursor.execute('SELECT attribute FROM attributes WHERE product_id = ? ORDER BY priority', (product_id,))
        attributes = cursor.fetchall()
        selected_attributes = [row['attribute'] for row in attributes]
        st.session_state["selected_attributes"] = selected_attributes

        conn.close()

        if "long_description" not in st.session_state:
            openai_prompt = f"""
            Generate a product description with the USPs mentioned. Start with a paragraph of information which is firstly, not same as the USPs,and secondly, not more than 60 words from the following : the problem the product solves for the customer, where and when is the customer going to use the product, how is the product better than other products in the market for the buyer? How does the product work to solve the problem of the buyers? Then, add the USPs mentioned, but do not use the term USPs and make each USP title appear in bold. Do not change the description of the USPs. Use Simple language understood by a grade 5 student) but retains important terms or keywords about the {product_name} product.
            {chr(10).join(selected_attributes)}
            """

            with st.spinner("Generating long product description..."):
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                        {"role": "user", "content": openai_prompt}
                    ]
                )

                long_description = completion.choices[0].message.content
                st.session_state["long_description"] = long_description

        long_description = st.session_state["long_description"]

        st.subheader("Long Product Description:")

        # Check if the user is in "edit mode"
        if "edit_mode" not in st.session_state:
            st.session_state["edit_mode"] = False

        if st.session_state["edit_mode"]:
            # Show text box for editing the description
            long_description = st.text_area("Edit Description:", value=long_description, height=300)

            if st.button("Save Edited Description"):
                st.session_state["long_description"] = long_description
                st.session_state["edit_mode"] = False
                st.success("Description updated!")
                st.rerun()
        else:
            # Show description as markdown
            st.markdown(st.session_state["long_description"])

            if st.button("Edit"):
                st.session_state["edit_mode"] = True
                st.rerun()

        if st.button("Save Long Description"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                REPLACE INTO descriptions (product_id, long_description)
                VALUES (?, ?)
            ''', (product_id, long_description))
            conn.commit()
            conn.close()
            st.success("Long description saved!")
            # st.rerun()

        # Layout with two columns for buttons
        col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


        with col1:
            # Continue to Page 4
            if st.button("Continue"):
                st.session_state.current_page = "Page 4"
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.current_page = "Page 6"
                st.rerun()

        
    else:
        st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")







elif st.session_state.current_page == "Page 4":
    st.title("Short Product Description-Bullets")

    product_id = st.session_state.get("product_id")
    if product_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch product name
        cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
        product_name_row = cursor.fetchone()
        if product_name_row:
            product_name = product_name_row['name']
            st.session_state["product_name"] = product_name
        else:
            st.error("Product name not found in the database.")
            st.stop()

        # Fetch long product description
        cursor.execute('SELECT long_description FROM descriptions WHERE product_id = ?', (product_id,))
        long_description_row = cursor.fetchone()
        if long_description_row:
            long_description = long_description_row['long_description']
            st.session_state["long_description"] = long_description
        else:
            st.error("Long description not found in the database.")
            st.stop()

        conn.close()

        if "short_description_bullets" not in st.session_state:
            openai_prompt = f"""
            Create a much shorter version of the following product description in which the initial paragraph is about half as long as the original and each USP description is about half as long. Keep the USP titles as is. 
            {long_description}
            """

            with st.spinner("Generating short product description..."):
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                        {"role": "user", "content": openai_prompt}
                    ]
                )

                short_description_bullets = completion.choices[0].message.content
                st.session_state["short_description_bullets"] = short_description_bullets

        short_description_bullets = st.session_state["short_description_bullets"]

        st.subheader("Short Product Description Bullets:")

        # Check if the user is in "edit mode"
        if "edit_mode_bullets" not in st.session_state:
            st.session_state["edit_mode_bullets"] = False

        if st.session_state["edit_mode_bullets"]:
            # Show text box for editing the description
            short_description_bullets = st.text_area("Edit Description Bullets:", value=short_description_bullets, height=300)

            if st.button("Save Edited Description Bullets"):
                st.session_state["short_description_bullets"] = short_description_bullets
                st.session_state["edit_mode_bullets"] = False
                st.success("Short description bullets updated!")
                st.rerun()
        else:
            # Show description as markdown
            st.markdown(st.session_state["short_description_bullets"])

            if st.button("Edit Description Bullets"):
                st.session_state["edit_mode_bullets"] = True
                st.rerun()

        if st.button("Save Short Description Bullets"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                REPLACE INTO descriptions (product_id, long_description, short_description_bullets)
                VALUES (?, ?, ?)
            ''', (product_id, long_description, short_description_bullets))
            conn.commit()
            conn.close()
            st.success("Short description saved!")
            # st.rerun()

        # Layout with two columns for buttons
        col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


        with col1:
            # Continue to Page 5
            if st.button("Continue"):
                st.session_state.current_page = "Page 5"
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.current_page = "Page 6"
                st.rerun()

    else:
        st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")




elif st.session_state.current_page == "Page 5":
    st.title("Short Product Description-Paragraph")

    product_id = st.session_state.get("product_id")
    if product_id:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch product name
        cursor.execute('SELECT name FROM products WHERE id = ?', (product_id,))
        product_name_row = cursor.fetchone()
        if product_name_row:
            product_name = product_name_row['name']
            st.session_state["product_name"] = product_name
        else:
            st.error("Product name not found in the database.")
            st.stop()

        # Fetch long product description
        cursor.execute('SELECT long_description FROM descriptions WHERE product_id = ?', (product_id,))
        long_description_row = cursor.fetchone()
        if long_description_row:
            long_description = long_description_row['long_description']
            st.session_state["long_description"] = long_description
        else:
            st.error("Long description not found in the database.")
            st.stop()

        # Fetch short product description (bullets)
        cursor.execute('SELECT short_description_bullets FROM descriptions WHERE product_id = ?', (product_id,))
        short_description_row = cursor.fetchone()
        if short_description_row:
            short_description_bullets = short_description_row['short_description_bullets']
            st.session_state["short_description_bullets"] = short_description_bullets
        else:
            st.error("Short description bullets not found in the database.")
            st.stop()

        conn.close()

        if "short_description_paragraph" not in st.session_state:
            openai_prompt = f"""
            Rewrite the below short product description in paragraph form. Keep the USPs in bold letters in sentence case.
            {short_description_bullets}
            """

            with st.spinner("Generating short product description..."):
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates product descriptions."},
                        {"role": "user", "content": openai_prompt}
                    ]
                )

                short_description_paragraph = completion.choices[0].message.content
                st.session_state["short_description_paragraph"] = short_description_paragraph

        short_description_paragraph = st.session_state["short_description_paragraph"]

        st.subheader("Short Product Description Paragraph:")

        # Check if the user is in "edit mode"
        if "edit_mode_paragraph" not in st.session_state:
            st.session_state["edit_mode_paragraph"] = False

        if st.session_state["edit_mode_paragraph"]:
            # Show text box for editing the description paragraph
            short_description_paragraph = st.text_area("Edit Description Paragraph:", value=short_description_paragraph, height=300)

            if st.button("Save Edited Description Paragraph"):
                st.session_state["short_description_paragraph"] = short_description_paragraph
                st.session_state["edit_mode_paragraph"] = False
                st.success("Short description paragraph updated!")
                st.rerun()
        else:
            # Show description as markdown
            st.markdown(st.session_state["short_description_paragraph"])

            if st.button("Edit Description Paragraph"):
                st.session_state["edit_mode_paragraph"] = True
                st.rerun()

        if st.button("Save Short Description Paragraph"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''
                REPLACE INTO descriptions (product_id, long_description, short_description_bullets, short_description_paragraph)
                VALUES (?, ?, ?, ?)
            ''', (product_id, long_description, short_description_bullets, short_description_paragraph))
            conn.commit()
            conn.close()
            st.success("Short description saved!")

        # Layout with two columns for buttons
        col1, col2 = st.columns([8, 2])  # Adjust column widths as needed


        with col1:
            # Continue to Page 6
            if st.button("Continue"):
                st.session_state.current_page = "Page 6"
                st.rerun()

        with col2:
            if st.button("Cancel"):
                st.session_state.current_page = "Page 6"
                st.rerun()


    else:
        st.error("Product ID not found. Please go back to Page 1 and proceed through the steps.")



elif st.session_state.current_page == "Page 6":
    st.title("Product Details and Descriptions")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch all products with their details and descriptions
    cursor.execute('''
        SELECT p.id, p.name, d.long_description, d.short_description_bullets, d.short_description_paragraph
        FROM products p
        LEFT JOIN descriptions d ON p.id = d.product_id
    ''')
    products = cursor.fetchall()

    if products:
        for product in products:
            product_id, product_name, long_description, short_description_bullets, short_description_paragraph = product

            st.write(f"**Product Name:** {product_name}")

            # Expandable sections for descriptions
            with st.expander("Long Description"):
                st.write(long_description if long_description else "No long description available.")

            with st.expander("Short Description (Bullets)"):
                st.write(short_description_bullets if short_description_bullets else "No short description (bullets) available.")

            with st.expander("Short Description (Paragraph)"):
                st.write(short_description_paragraph if short_description_paragraph else "No short description (paragraph) available.")

            # Delete button for each product
            if st.button(f"Delete {product['name']}"):
                delete_product(product['id'])
                st.success(f"Product '{product['name']}' has been deleted.")
                st.rerun()  # Refresh the page to reflect the deletion
                
            st.write("---")  # Separator between products

    conn.close()

    if st.button("Add New Product"):
        if "product_id" in st.session_state:
            del st.session_state["product_id"]
        if "product_name" in st.session_state:
            del st.session_state["product_name"]
        if "selected_attributes" in st.session_state: 
            del st.session_state["selected_attributes"]
        if "generated_description" in st.session_state: 
            del st.session_state["generated_description"]
        if "long_description" in st.session_state: 
            del st.session_state["long_description"]
        if "short_description_bullets" in st.session_state:  
            del st.session_state["short_description_bullets"]
        if "short_description_paragraph" in st.session_state:  
            del st.session_state["short_description_paragraph"]




        st.session_state.usps = []
        st.session_state.attributes = []
        st.session_state.descriptions = []
        st.session_state.attributes = []

        st.session_state.current_page = "Page 1"
        st.write("Redirecting to Page 1...")
        st.rerun()

