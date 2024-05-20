pip install streamlit

import streamlit as st
import pandas as pd
import json

# Placeholder to store events
if 'events' not in st.session_state:
    st.session_state['events'] = []

# Streamlit form
with st.form(key='user_input_form'):
    card_type = st.radio("Card Type:", ['Visa', 'Mastercard', 'Discover', 'JCB'])
    name = st.text_input("Your Name")
    card_number = st.text_input("Your Card Number")
    cvc = st.text_input("CVC")
    expiry = st.text_input("Expiry MM/YY")
    submit_button = st.form_submit_button("Pay Now")

# JavaScript to capture events and send them to Streamlit
js_code = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.stForm');
    form.addEventListener('keydown', (event) => {
        // Post keydown event to Streamlit
        const message = {type: 'keydown', key: event.key, time: Date.now()};
        parent.postMessage({type: 'streamlit:setComponentValue', key: 'events', value: JSON.stringify(message)}, '*');
    });

    form.addEventListener('keyup', (event) => {
        // Post keyup event to Streamlit
        const message = {type: 'keyup', key: event.key, time: Date.now()};
        parent.postMessage({type: 'streamlit:setComponentValue', key: 'events', value: JSON.stringify(message)}, '*');
    });

    // Add mouse event listeners if needed
});

// Add a handler for Streamlit events
window.addEventListener("message", (event) => {
    const {type, key, value} = event.data;
    if (type === 'streamlit:formSubmit') {
        // Clear events on form submit
        Streamlit.setComponentValue('events', []);
    }
});
</script>
"""
st.markdown(js_code, unsafe_allow_html=True)

# Handle event logging
event_data = st.text_input("Event log (hidden)", "", key='events', on_change=lambda: st.session_state['events'].append(json.loads(st.session_state['events'])))
st.write("Logged Events:", st.session_state['events'])

# Compute metrics when form is submitted
if submit_button:
    events_df = pd.DataFrame(st.session_state['events'])
    # Process the events_df to compute dwell time, flight time, and trajectory
    # Example: Calculate dwell times
    dwell_times = events_df[events_df['type'] == 'keyup'].time - events_df[events_df['type'] == 'keydown'].time.shift(1)
    st.write("Average Dwell Time:", dwell_times.mean())
    # Reset or clear events after processing
    st.session_state['events'] = []

