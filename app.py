import streamlit as st

st.set_page_config(
    page_title="Dental Progress Notes Generator",
    page_icon="🦷",
    layout="wide"
)

st.title("🦷 Dental Clinical Note Assistant")
st.caption("Standardized documentation generator for Kiwi Health Progress Notes")

# Procedure selection
procedure = st.radio(
    "Select Procedure:",
    ["Root Canal Treatment (RCT)", "Restoration / Filling"],
    horizontal=True
)

col1, col2 = st.columns([1, 1], gap="medium")

# Canal configuration logic based on FDI tooth numbering
def get_canals_for_tooth(tooth_str):
    try:
        tooth = int(tooth_str)
    except ValueError:
        return ["Canal 1"]
        
    if tooth in [16, 17, 26, 27]:
        return ["Mesiobuccal Canal", "Distobuccal Canal", "Palatal Canal"]
    elif tooth in [36, 37, 46, 47]:
        return ["Mesiobuccal Canal", "Mesiolingual Canal", "Distal Canal"]
    elif tooth in [14, 15, 24, 25]:
        return ["Buccal Canal", "Palatal Canal"]
    elif tooth in [34, 35, 44, 45]:
        return ["Main Canal", "Second Canal (if present)"]
    else:
        return ["Single Canal"]

with col1:
    st.subheader("Clinical Inputs")
    tooth_number = st.text_input("Tooth Number (FDI):", value="16")
    
    if procedure == "Root Canal Treatment (RCT)":
        canals = get_canals_for_tooth(tooth_number)
        st.write(f"**Detected Anatomy:** {', '.join(canals)}")
        
        canal_data = []
        for idx, canal_name in enumerate(canals):
            st.markdown(f"**{canal_name}**")
            c_len, c_file = st.columns(2)
            with c_len:
                length_val = st.text_input(f"Working Length", value="21 mm", key=f"len_{idx}")
            with c_file:
                file_val = st.text_input(f"File Size", value="25/04", key=f"file_{idx}")
            canal_data.append((canal_name, length_val, file_val))
            
        dressing = st.text_input("Dressing:", value="Calcium Hydroxide paste + Cavit temp")
        advice = st.text_input("Advice / Next Appointment:", value="Avoid hard food on right side. Recall after 5 days for obturation.")

    else:
        rest_class = st.text_input("Class / Surface:", value="Class II (MOD)")
        material = st.text_input("Material:", value="Composite Resin")
        shade = st.text_input("Shade:", value="A2")
        bonding = st.text_input("Bonding Agent & Etching:", value="Total-etch 37% Phosphoric acid + Universal Adhesive")

# Generate Note Preview
with col2:
    st.subheader("Kiwi Health Note Preview")
    
    if procedure == "Root Canal Treatment (RCT)":
        note_text = f"ROOT CANAL TREATMENT (RCT)\n"
        note_text += f"Tooth: #{tooth_number}\n\n"
        note_text += f"CANAL MEASUREMENTS:\n"
        for c_name, c_l, c_f in canal_data:
            note_text += f"• {c_name}: Working Length: {c_l or '__ mm'} | File Size: {c_f or '__'}\n"
        note_text += f"\nDressing: {dressing or 'None'}\n"
        note_text += f"Advice: {advice or 'Routine post-op precautions'}"
    else:
        note_text = f"RESTORATION / FILLING\n"
        note_text += f"Tooth: #{tooth_number}\n"
        note_text += f"Class / Surface: {rest_class or '__'}\n"
        note_text += f"Material: {material or '__'}\n"
        note_text += f"Shade: {shade or '__'}\n"
        note_text += f"Bonding Agent & Etching: {bonding or '__'}"

    # Text area for easy copying
    st.text_area("Generated Note (Select All & Copy):", value=note_text, height=260)
    
    # Direct code snippet with built-in copy icon
    st.markdown("**Click top-right copy icon below to copy directly:**")
    st.code(note_text, language="text")