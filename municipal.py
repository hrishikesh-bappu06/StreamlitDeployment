
import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import os
import uuid # For generating unique ticket IDs
import time


st.set_page_config(page_title="Municipal Issue Reporter", page_icon="data:image/jpeg;base64,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")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY","AIzaSyA-10Y9sMjvOZ3pemciGWXkhGcrFnD619k")

if not GOOGLE_API_KEY:
    st.error("🚨 Google API Key not found. Please set it in Streamlit secrets or a .env file.")
    st.stop() # Halt execution if no API key

# Configure the generative AI model
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"🚨 Error configuring Google AI: {e}")
    st.stop()

# --- Helper Functions ---

def get_gemini_vision_response(image_data, prompt):
    """Analyzes the image using Gemini Vision model."""
    try:
        # Ensure image_data is bytes
        if isinstance(image_data, Image.Image):
             buffered = io.BytesIO()
             # Convert RGBA to RGB if necessary, as JPEG doesn't support alpha
             if image_data.mode == 'RGBA':
                 image_data = image_data.convert('RGB')
             image_data.save(buffered, format="JPEG")
             img_bytes = buffered.getvalue()
        elif isinstance(image_data, bytes):
             img_bytes = image_data
        else:
             st.error("Invalid image data type for Gemini.")
             return None

        image_parts = [{"mime_type": "image/jpeg", "data": img_bytes}]
        response = vision_model.generate_content([prompt, image_parts[0]], stream=False)
        response.resolve()
        return response.text
    except Exception as e:
        st.error(f"⚠️ Error analyzing image with Gemini: {e}")
        print(f"Gemini Error: {e}") # Debugging
        return None

def generate_ticket_id():
    """Generates a unique ticket ID."""
    return f"TKT-{uuid.uuid4().hex[:8].upper()}"

# --- Add message to chat history ---
def add_message(role, content, image=None, update_state=True):
    """Adds a message to the session state chat log."""
    message = {"role": role, "content": content}
    # Ensure image is PIL Image for display if passed
    display_image = None
    if image:
        if isinstance(image, bytes):
            try:
                display_image = Image.open(io.BytesIO(image))
            except Exception:
                 print("Could not open image bytes for display.")
        elif isinstance(image, Image.Image):
             display_image = image

    if display_image:
        message["image"] = display_image

    if update_state:
        st.session_state.messages.append(message)
    # print(f"Added message: Role={role}, Stage={st.session_state.get('stage', 'N/A')}") # Debug
    return message # Return message dict for immediate display if needed

# --- Reset state function ---
def reset_conversation(reason=""):
    """Clears session state to restart the conversation."""
    print(f"Resetting conversation. Reason: {reason}") # Debug
    # Keep the initial welcome message?
    welcome_message = {"role": "assistant", "content": "Welcome! Please describe the municipal issue you'd like to report, or upload an image of it."}
    reset_msg = {"role": "assistant", "content": f"{reason} You can start a new report now."}

    # Clear all keys except maybe 'messages' initially
    keys_to_clear = list(st.session_state.keys())
    for key in keys_to_clear:
        if key != 'messages': # Avoid modifying while iterating if possible
             del st.session_state[key]

    # Reset specific state variables cleanly
    st.session_state.messages = [welcome_message]
    if reason:
        st.session_state.messages.append(reset_msg)
    st.session_state.stage = "start"
    st.session_state.current_image_bytes = None
    st.session_state.current_image_display = None
    st.session_state.analysis_result = None
    st.session_state.suggested_issue = None
    st.session_state.confirmed_issue = None
    st.session_state.user_details = {"name": None, "contact": None, "location": None, "comments": None}
    st.session_state.ticket_id = None
    st.session_state.last_processed_file_id = None # Crucial reset

# --- Streamlit App UI ---
st.title("Municipal Issue Reporting Chatbot")

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Welcome! Please describe the municipal issue you'd like to report, or upload an image of it."}]
if "stage" not in st.session_state:
    st.session_state.stage = "start"
if "current_image_bytes" not in st.session_state:
     st.session_state.current_image_bytes = None
if "current_image_display" not in st.session_state:
     st.session_state.current_image_display = None
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "suggested_issue" not in st.session_state:
    st.session_state.suggested_issue = None
if "confirmed_issue" not in st.session_state:
    st.session_state.confirmed_issue = None
if "user_details" not in st.session_state:
    st.session_state.user_details = {"name": None, "contact": None, "location": None, "comments": None}
if "ticket_id" not in st.session_state:
    st.session_state.ticket_id = None
if "last_processed_file_id" not in st.session_state:
     st.session_state.last_processed_file_id = None # Track the ID of the last processed file

# --- Display Chat History ---
# Use a container for chat messages to allow input area below
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message and message["image"]:
                st.image(message["image"], caption="Uploaded Image" if message['role'] == 'user' else "Issue Image", width=200)
            st.markdown(message["content"])


# --- Define Input Area ---
# Place the file uploader above the text input for better visual separation
uploaded_file = st.file_uploader(
    "Upload an image of the issue (Optional)", # Restore descriptive label
    type=["jpg", "jpeg", "png"],
    key="file_uploader_key_" + str(st.session_state.get('last_processed_file_id', '0')), # Attempt to force refresh key on reset
    help="Drag and drop or browse to upload an image file."
)

user_input = st.chat_input("Your message...")


# --- Core Logic ---
# Determine if a new file has been uploaded in this cycle
new_file_uploaded_this_run = False
if uploaded_file is not None:
    # Use file_id for robust checking against reruns
    current_file_id = uploaded_file.file_id
    if current_file_id != st.session_state.get('last_processed_file_id', None):
        new_file_uploaded_this_run = True
        print(f"Detected new file upload: {uploaded_file.name} (ID: {current_file_id})") # Debug


# 1. Process NEW Image Upload First (if any)
if new_file_uploaded_this_run:
    current_stage = st.session_state.stage
    # Allow image upload primarily at the start
    if current_stage == "start":
        try:
            image = Image.open(uploaded_file)
            # Store image data before potential failures/reruns
            st.session_state.current_image_display = image
            img_byte_arr = io.BytesIO()
            save_format = image.format if image.format in ['JPEG', 'PNG'] else 'JPEG'
            # Convert RGBA to RGB if necessary
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            image.save(img_byte_arr, format=save_format)
            st.session_state.current_image_bytes = img_byte_arr.getvalue()

            # Display user's upload message immediately *in the main chat container*
            with chat_container: # Ensure message appears in the correct place
                 user_msg = add_message("user", f"Uploaded image: {uploaded_file.name}", image=st.session_state.current_image_display)
                 with st.chat_message(user_msg["role"]):
                     if user_msg.get("image"): st.image(user_msg["image"], caption="Uploaded Image", width=200)
                     st.markdown(user_msg["content"])

            # Mark as processed immediately using file_id
            st.session_state.last_processed_file_id = current_file_id

            # Analyze the image
            prompt_vision = """Analyze this image regarding a potential municipal issue (e.g., 'pothole', 'pile of garbage', 'broken streetlight', 'water logging', 'damaged sidewalk', 'other'). Be concise. Describe what you see and suggest one likely issue category. If unsure, say 'Unclear issue'. Example Response: 'Looks like a pothole. Suggested issue: Road Damage'"""

            with st.spinner("Analyzing image..."):
                analysis = get_gemini_vision_response(st.session_state.current_image_bytes, prompt_vision)

            if analysis:
                st.session_state.analysis_result = analysis
                if "Suggested issue:" in analysis:
                    st.session_state.suggested_issue = analysis.split("Suggested issue:")[-1].strip()
                    question = f"Assistant: {analysis}\n\nIs '{st.session_state.suggested_issue}' the correct issue type? (Type 'yes' or 'no', or describe the issue differently)"
                else: # Unclear or no suggestion
                    st.session_state.suggested_issue = None
                    question = f"Assistant: {analysis}\n\nOkay, I've analyzed the image. Could you please describe the specific issue you want to report based on this image?"

                add_message("assistant", question)
                st.session_state.stage = "awaiting_confirmation_or_description"
            else:
                add_message("assistant", "Assistant: Sorry, I couldn't analyze the image properly. Can you please describe the issue instead?")
                st.session_state.stage = "awaiting_manual_description"

            st.rerun() # Rerun to display the analysis/question

        except Exception as e:
            st.error(f"Error processing image: {e}")
            add_message("assistant", "Assistant: There was an error processing the image file. Please try again or describe the issue.")
            # Mark as processed even on error to avoid loop
            st.session_state.last_processed_file_id = current_file_id
            st.session_state.stage = "start" # Reset stage
            st.rerun()
    else:
        # If user uploads image when not in 'start' stage
        add_message("assistant", "Assistant: Please respond to the current question first. You can upload a new image if you start over.")
        # Mark as processed to prevent loop on this stale file
        st.session_state.last_processed_file_id = current_file_id
        st.rerun()


# 2. Process Text Input (only if no NEW image was processed in this run)
elif user_input:
    # Display user message *in the main chat container*
    with chat_container:
        user_msg = add_message("user", user_input)
        with st.chat_message(user_msg["role"]):
            st.markdown(user_msg["content"])

    current_stage = st.session_state.stage
    next_stage = current_stage # Default: remain in the same stage
    rerun_needed = False

    # --- State Machine Logic based on Text Input ---
    if current_stage == "start":
        if len(user_input.split()) <= 2 and user_input.lower().strip() in ["hi", "hello", "hey", "greetings", "yo", "ok", "okay"]:
             add_message("assistant", "Assistant: Hello! To report an issue, please describe it or upload an image.")
             rerun_needed = True # Need to show the assistant's reply
        elif len(user_input.split()) < 3:
             add_message("assistant", "Assistant: Could you please provide a bit more detail about the issue you want to report?")
             rerun_needed = True
        else:
            st.session_state.confirmed_issue = user_input.strip()
            add_message("assistant", f"Assistant: Understood. You want to report: '{st.session_state.confirmed_issue}'.\n\nNow, what is your name?")
            next_stage = "collect_name"

    elif current_stage == "awaiting_confirmation_or_description":
        lower_input = user_input.lower().strip()
        if "yes" in lower_input and st.session_state.suggested_issue:
            st.session_state.confirmed_issue = st.session_state.suggested_issue
            add_message("assistant", f"Assistant: Great! Reporting as '{st.session_state.confirmed_issue}'.\n\nWhat is your name?")
            next_stage = "collect_name"
        elif "no" in lower_input:
            add_message("assistant", "Assistant: Okay. Please describe the specific issue you see in the image or want to report.")
            next_stage = "awaiting_manual_description"
        else: # User provided their own description
            st.session_state.confirmed_issue = user_input.strip()
            if len(st.session_state.confirmed_issue) < 5: # Basic check
                 add_message("assistant", "Assistant: Please provide a more detailed description of the issue.")
                 # Stay in this stage (next_stage = current_stage)
                 rerun_needed = True
            else:
                 add_message("assistant", f"Assistant: Understood. Reporting as '{st.session_state.confirmed_issue}'.\n\nWhat is your name?")
                 next_stage = "collect_name"

    elif current_stage == "awaiting_manual_description":
        if len(user_input.split()) < 3:
            add_message("assistant", "Assistant: Could you please provide a bit more detail about the issue?")
            rerun_needed = True
        else:
            st.session_state.confirmed_issue = user_input.strip()
            add_message("assistant", f"Assistant: Got it. Reporting issue: '{st.session_state.confirmed_issue}'.\n\nWhat is your name?")
            next_stage = "collect_name"

    elif current_stage == "collect_name":
        name = user_input.strip()
        if len(name) > 1:
            st.session_state.user_details["name"] = name
            add_message("assistant", "Assistant: Thanks! Please provide your contact information (phone or email).")
            next_stage = "collect_contact"
        else:
             add_message("assistant", "Assistant: Please enter a valid name.")
             rerun_needed = True

    elif current_stage == "collect_contact":
        contact = user_input.strip()
        # Simple check for plausibility (adjust as needed)
        if len(contact) > 5 and ("@" in contact or any(c.isdigit() for c in contact)):
            st.session_state.user_details["contact"] = contact
            add_message("assistant", "Assistant: Great. Now, please provide the location of the issue (e.g., address, nearest landmark, or cross-streets).")
            next_stage = "collect_location"
        else:
            add_message("assistant", "Assistant: Please enter a valid phone number or email address.")
            rerun_needed = True

    elif current_stage == "collect_location":
        location = user_input.strip()
        if len(location) > 5: # Basic check
            st.session_state.user_details["location"] = location
            add_message("assistant", "Assistant: Almost done! Any additional comments or details? (You can type 'None' if there are none)")
            next_stage = "collect_comments"
        else:
            add_message("assistant", "Assistant: Please provide a more specific location.")
            rerun_needed = True

    # ############################################### #
    # ## THIS IS THE UPDATED SUMMARY SECTION BELOW ## #
    # ############################################### #
    elif current_stage == "collect_comments":
        st.session_state.user_details["comments"] = user_input.strip()

        # --- Prepare Nicer Confirmation Summary ---
        # Use .get() for safer access to potentially missing keys
        # Use st.session_state.get() for top-level state keys if needed
        issue_val = st.session_state.get('confirmed_issue', '*Unknown Issue*')
        name_val = st.session_state.user_details.get('name', '*Not Provided*')
        contact_val = st.session_state.user_details.get('contact', '*Not Provided*')
        location_val = st.session_state.user_details.get('location', '*Not Provided*')
        comments_val = st.session_state.user_details.get('comments', '*None*')
        # Handle empty comments specifically to show '*None*' instead of just empty
        if not comments_val or comments_val.lower() == 'none':
            comments_val = '*None*'

        summary = f"""**Please review the details before submission:**

        *Issue Reported:-- `{issue_val}`
        *Your Name:-- {name_val}
        *Contact Info:-- {contact_val}
        *Issue Location:-- {location_val}
        *Additional Comments:-- {comments_val}
        """
        # --- End of Summary Preparation ---

        confirmation_message = f"Assistant: Okay, here's a summary:\n\n{summary}\n\nIf everything is correct, please type **'confirm'** to submit. Type **'cancel'** to restart."
        # Add summary message, include image if available
        add_message("assistant", confirmation_message, image=st.session_state.current_image_display)
        next_stage = "confirm_details"
    # ############################################### #
    # ## END OF UPDATED SUMMARY SECTION            ## #
    # ############################################### #

    elif current_stage == "confirm_details":
        lower_input = user_input.lower().strip()
        if "confirm" in lower_input:
            st.session_state.ticket_id = generate_ticket_id()
            # --- Simulate Submission ---
            print("--- Ticket Submitted ---")
            print(f"Ticket ID: {st.session_state.ticket_id}")
            print(f"Issue: {st.session_state.confirmed_issue}") # Use confirmed_issue directly
            print(f"Name: {st.session_state.user_details.get('name', 'N/A')}")
            print(f"Contact: {st.session_state.user_details.get('contact', 'N/A')}")
            print(f"Location: {st.session_state.user_details.get('location', 'N/A')}")
            # Use the formatted comments_val logic if needed for printing, or raw data
            print(f"Comments: {st.session_state.user_details.get('comments', 'N/A')}")
            print(f"Image Submitted: {'Yes' if st.session_state.current_image_bytes else 'No'}")
            print("----------------------")
            # --- End Simulation ---

            
            success_message = f"""Assistant: Thank you for reporting! ✅
            Your ticket has been created with ID: **{st.session_state.ticket_id}**
            Our team will review the issue reported at '{st.session_state.user_details.get('location', '*Location Not Provided*')}' shortly.
            Type 'new report' to start another one."""
            add_message("assistant", success_message)
            
            
            next_stage = "submitted"

        elif "cancel" in lower_input:
            reset_conversation(reason="Report cancelled.")
            rerun_needed = True # Rerun to show the cleared state and message
        else:
            add_message("assistant", "Assistant: Please type 'confirm' or 'cancel' to proceed.")
            rerun_needed = True

    elif current_stage == "submitted":
        if "new report" in user_input.lower().strip():
             reset_conversation(reason="Starting new report.")
             rerun_needed = True
        else:
            add_message("assistant", "Assistant: Your previous report was submitted. To start a new report, please type 'new report'.")
            rerun_needed = True

    # Update stage and rerun if stage changed OR if a rerun is explicitly needed
    if next_stage != current_stage:
        st.session_state.stage = next_stage
        rerun_needed = True # Always rerun if stage changes

    if rerun_needed:
      st.rerun()
