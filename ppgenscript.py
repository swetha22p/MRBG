import pandas as pd
import requests
from io import StringIO

# Use the correct CSV export URL from Google Sheets
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQGHN53_dTmJlwfR8Tbc-cEficBnw--wEDIlOeY11pdpL5WAh3aJbpXz8Yg5y8vEDcLe4n4hIIVGtRP/pub?gid=0&single=true&output=csv"

response = requests.get(csv_url)

if response.status_code == 200:
    data = StringIO(response.text)
    df = pd.read_csv(data)

    # Clean column names
    df.columns = df.columns.str.strip().str.lower()
    print("Cleaned columns:", df.columns.tolist())

    output_lines = []

    # Start writing the function definition
    output_lines.append("def get_ppost(datacase, cond=None, data_seman=None, root_main=None, concept_type=None):")
    output_lines.append("    ppost = ''\n")

    # Track whether we've written the first condition (to use 'if' then 'elif')
    first_condition = True

    for _, row in df.iterrows():
        key_raw = str(row['key']).strip()
        value = str(row['value']).strip()
        condition = str(row.get('cond', '')).strip()

        keys = [k.strip() for k in key_raw.split(',') if k.strip()]

        # Generate condition line
        if len(keys) == 1:
            condition_line = f"datacase == '{keys[0]}'"
        else:
            formatted_keys = ', '.join([repr(k) for k in keys])
            condition_line = f"datacase in ({formatted_keys})"

        # Use 'if' for first, 'elif' for others
        if first_condition:
            output_lines.append(f"    if {condition_line}:")
            first_condition = False
        else:
            output_lines.append(f"    elif {condition_line}:")  # Chained conditions

        # Handle nested condition if present
        if condition and condition.lower() != 'nan':
            output_lines.append(f"        if {condition}:")
            output_lines.append(f"            ppost = '{value}'")
        else:
            output_lines.append(f"        ppost = '{value}'")

        output_lines.append("")  # blank line between conditions

    # Final return statement
    output_lines.append("    return ppost")

    # Save to file
    with open("generated_conditions.py", "w") as f:
        f.write("\n".join(output_lines))

    print("✅ Logic successfully generated and saved in 'generated_conditions.py'")
else:
    print(f"❌ Failed to fetch CSV. Status code: {response.status_code}")