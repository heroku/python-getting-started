import numpy as np
import pandas as pd
import csv
import gender_guesser.detector as gender
import requests, re, json, spacy

MALE_GENDER = 0
FEMALE_GENDER = 1
OTHER_OR_UNKNOWN_GENDER = 2

CURRENT_YEAR = 2025

BASELINE_WOMEN_LEVELS = {
    "gaba": 0,
    "dopamine": -0.2,
    "oxytocin": 0.2,
    "serotonin": 0.1,
    "glutamine": -0.1,
}

BASELINE_OLD_AGE_LEVELS = {
    "gaba": -0.1,
    "dopamine": -0.2,
    "oxytocin": 0.1,
    "serotonin": -0.2,
    "glutamine": 0.2,
}

NEUROTRANSMITTERS = ['gaba', 'dopamine', 'oxytocin', 'serotonin', 'glutamine']
SAMPLE_DATA_FILE_PATH = 'Aaron.csv'

NATIONALITY_LIKELYHOOD_THRESHOLD = 0.2
d = gender.Detector()

# TODO: Add more complex mappings based on research
NEUROTRANSMITTERS_WORD_ASSOCIATION = {
    'gaba': ['calm', 'relaxation', 'peace', 'inhibition', 'unwind', 'gaba'],
    'dopamine': ['reward', 'motivation', 'energy', 'dopamine'],
    'oxytocin': ['bonding', 'trust', 'social', 'connection', 'oxytocin'],
    'serotonin': ['clarity', 'focus', 'sharp', 'productive', 'serotonin'],
    'glutamine' : ['memory', 'learning', 'cognition', 'glutamine'],
    # Add more complex mappings here based on your research
}

# To map scent words (as opposed to recorded behavior) to neurotransmitter states
SCENT_WORD_ASSOCIATION = {
    'gaba': ['gaba'],
    'oxytocin': ['oxytocin'],
    'dopamine': ['dopamine'],
    'serotonin': ['serotonin'],
    'glutamine': ['glutamine'],
}


SPLITTER_REGEX = r'[,;]|\bat\b'


def load_spacy_model():
    """
    Loads the spaCy NLP model for text processing.
    
    :return: Loaded spaCy NLP model.
    """
    try:
        nlp = spacy.load("en_core_web_md")
        print("spaCy model loaded successfully.")
        return nlp
    except OSError:
        print("spaCy model not found. Downloading...")
        spacy.cli.download("en_core_web_md")
        nlp = spacy.load("en_core_web_md")
        print("spaCy model downloaded and loaded successfully.")
        return nlp



NLP_MODEL = load_spacy_model()
EXAMPLE_STRESSORS = ['lack of communication', 'managerial conflict', 'heavy workload', 'job insecurity', 'burnout']


def read_csv(file_path):
    """
    Reads a CSV file and returns its content as a list of dictionaries.
    
    :param file_path: Path to the CSV file.
    :return: List of dictionaries representing the CSV rows.
    """
    with open(file_path, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

def write_csv(file_path, data):
    """
    Writes a list of dictionaries to a CSV file.
    
    :param file_path: Path to the CSV file.
    :param data: List of dictionaries to write to the CSV file.
    """
    if not data:
        return  # No data to write
    
    with open(file_path, mode='w', encoding='utf-8', newline='') as csvfile:
        fieldnames = data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def print_imported_csv(file_path):
    """
    Prints the content of a CSV file.
    
    :param file_path: Path to the CSV file.
    """
    pd.set_option('display.max_columns', None)  # Show all columns in DataFrame
    data = pd.DataFrame(read_csv(file_path))  # Convert to numpy array if needed
    print(data)
    return data


def rename_columns(data):
    """
    Renames columns in the DataFrame to more descriptive names.
    
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with renamed columns.
    """
    data.rename(columns={
    'Please enter your name (optional) ': 'Full Name',
    'Please enter your current job title and company ': 'Current Job Title and Company',
    'If company was omitted above, please indicate what industry you operate within ': 'Industry',
    'Please enter your region (working)': 'Working Region',
    'Please enter a brief description of things you believe limit your productivity and performance in the workplace (ex. poor communication within teams, dislike of manager, etc.) ': 'Productivity Limitations',
    'Please enter a brief description of your career goals (ex. promotion, startup founder, etc. )': 'Career Goals',
    'What sex were you assigned at birth?': 'Sex',
    'Please enter your favorite perfume, cologne, or candle (enter n/a if this does not apply)': 'Favorite Scent',
    'Please describe a positive association you have with scent from childhood (ex. I remember my mom would make chicken pot pie and the smell of the crust always makes me nostalgic for that time) ': 'Positive Childhood Scent Association',
}, inplace=True)
    
    data = data[['Email Address', 'Full Name', 'Current Job Title and Company', 'Industry', 'Working Region',
             'Productivity Limitations', 'Career Goals', 'Sex', 'Favorite Scent',
             'Positive Childhood Scent Association']]

    return data



def get_age(name):
    """
    Fetches the age prediction for a given name using the Agify API.
    
    :param name: Name to predict age for.
    :return: Predicted age or None if the request fails.
    """
    try:
        response = requests.get(f'https://api.agify.io/?name={name}')
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        return data.get('age')
    except requests.RequestException as e:
        print(f"Error fetching age for {name}: {e}")
        return None
    
def fake_get_age(name):
    """
    A fake function to simulate age prediction for testing purposes.
    
    :param name: Name to predict age for.
    :return: A fixed age value (e.g., 30).
    """
    return 52  # Simulated fixed age for testing purposes

def get_nationality(name):
    """
    Fetches the nationality prediction for a given name using the Nationalize API.
    :param name: Last name to predict nationality for.
    :return: Predicted nationality or None if the request fails.
    """
    try:
        response = requests.get(f'https://api.nationalize.io/?name={name}')
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        if data['country']:
            if data['country'][0]['probability'] > NATIONALITY_LIKELYHOOD_THRESHOLD:
                # Return the country ID if the probability is greater than 0.5
                return data['country'][0]['country_id']
            else:
                # If no country has a high enough probability, return None
                return "unknown"
        return None
    except requests.RequestException as e:
        print(f"Error fetching nationality for {name}: {e}")
        return None


def check_for_year_in_string(s):
    """
    Checks if a string contains a year within the range of 1900 to the current year, using Regex.
    
    :param s: String to check for a year.
    :return: the year if found, otherwise None.
    """
    pattern = r'(19[0-9]{2}|20[0-2][0-9]|202[0-5])'
    return int(re.search(pattern, s).group(0)) if re.search(pattern, s) else None


def read_json(file_path):
    """
    Reads a JSON file and returns its content.
    
    :param file_path: Path to the JSON file.
    :return: Content of the JSON file.
    """
    with open(file_path, 'r', encoding='utf-8') as jsonfile:
        return json.load(jsonfile)
    


def check_for_gender_in_string(s):
    """
    Checks if a string contains a name in the list of common names given by SSN data(1990)
    TODO: RegExify this to make it more efficient

    :param s: String to check for a name.
    :return: the likely gender of the name if found, otherwise None.
    """
    names = read_json('markers.json')["names"]
    for name in names:
        if name.lower() in s.lower():
            return d.get_gender(name)
    return "unknown"  # Return "unknown" if no name is found


def check_for_professional_domain(s):
    """
    Checks if a string contains a professional domain (e.g., .com, .org, etc.)
    
    :param s: String to check for a professional domain.
    :return: the professional domain if found, otherwise None.
    """
    if s in read_json('markers.json')["personal-emails"]:
        return False
    return True

def check_for_occupation_in_string(s):
    """
    Checks if a string contains an occupation in the list of common occupations.
    TODO: RegExify this to make it more efficient
    
    :param s: String to check for an occupation.
    :return: the likely occupation if found, otherwise None.
    """
    if not s:
        return None
    occupations = read_json('markers.json')["professional-words"]
    for occupation in occupations:
        if occupation.lower() in s.lower():
            return occupation
    return None







def get_all_neurotransmitter_states(stressor_phrase, nlp_model, neurotransmitters):
    """
    Finds the closest neurotransmitter state based on the stressor phrase.
    
    :param stressor_phrase: The stressor phrase to analyze.
    :param nlp_model: The spaCy NLP model to use for vector similarity.
    :param neurotransmitters: Dictionary of neurotransmitter states and their associated words.
    :return: The all neurotransmitter states and their similarity scores.
    """
    doc_stressor = nlp_model(stressor_phrase)
    ans = list()
    
    if not doc_stressor.has_vector:
        return "N/A", -1  # No vector available for this phrase
    
    for nt_state, associated_words in neurotransmitters.items():
        doc_nt = nlp_model(" ".join(associated_words))
        
        if not doc_nt.has_vector:
            continue

        similarity = doc_stressor.similarity(doc_nt)
        ans.append((nt_state, similarity))

    # Sort by similarity score in descending order
    ans.sort(key=lambda x: x[1], reverse=True)
    return ans

def get_closest_neurotransmitter_state(stressor_phrase, nlp_model, neurotransmitters):
    return get_all_neurotransmitter_states(stressor_phrase, nlp_model, neurotransmitters)[0]

def find_closest_words(target_word, nlp):
    if nlp.vocab.has_vector(target_word):
        target_vector = nlp.vocab.get_vector(target_word)
        
        # Get all words in vocab with vectors
        all_words = []
        all_vectors = []
        for lexeme in nlp.vocab:
            if lexeme.has_vector and lexeme.is_alpha: # Only consider words that are alphabetic
                all_words.append(lexeme.text)
                all_vectors.append(lexeme.vector)
                
        # Calculate cosine similarity with all other words
        similarities = [nlp(target_word).similarity(nlp(word)) for word in all_words]

        # Sort and print top N
        sorted_words = sorted(zip(all_words, similarities), key=lambda x: x[1], reverse=True)
        
        print(f"Top 10 words most similar to '{target_word}':")
        return sorted_words[:10]
    else:
        print(f"'{target_word}' not found in spaCy's vocabulary or no vector available.")

def get_olfactory_profile(job):
    """
    Determines the olfactory profile based on the job title using neurotransmitter associations.
    
    :param job_title: Job title to determine the olfactory profile.
    :return: Olfactory profile as a string.
    """
    return get_all_neurotransmitter_states(job, NLP_MODEL, NEUROTRANSMITTERS_WORD_ASSOCIATION)



def extract_fingerprint_from_email(email_address):
    """
    Extracts any possible footprint information from an email address.

    Such information that we'd like to extract include:
    - Gender guess, if a first name appears in the email
    - Age guess, if a year of birth appears in the email
    TODO: Nationality guess, if a last name appears in the email
        * this seemed like more work than it was worth, so I left it out for now
    - Hints of occupation, if a job title appears in the email
    - Hints of industry, if an industry appears in the email
    - Hints of stress levels, if a job title appears in the email
    - Hints of an olfactory profile, if a job title appears that aligns with a user profile

    
    :param email: Email address to extract information from.
    :return: Dictionary containing extracted footprint information.
    """
    footprint = {
        "gender" : "unknown",
        "age" : None,
        "nationality" : None,
        "professional": None,
        "occupation" : None,
        "industry" : None,
        "stress_level" : None,
        "olfactory_profile" : None,        
    }

    email = {
        "local": email_address.split('@')[0],
        "domain": email_address.split('@')[1] if '@' in email_address else None
    }

    # We want to check if there is a number in the local part of the email, so we can guess the age
    footprint["age"] = CURRENT_YEAR - check_for_year_in_string(email["local"]) if check_for_year_in_string(email["local"]) else "unknown"
    footprint["gender"] = check_for_gender_in_string(email["local"])
    footprint["professional"] = check_for_professional_domain(email["domain"])
    footprint["occupation"] = check_for_occupation_in_string(email["local"])
    footprint["industry"] = check_for_occupation_in_string(email['domain'])
    if footprint["occupation"] or footprint['industry']:
        if footprint["occupation"] is None:
            footprint["occupation"] = footprint['industry']
        footprint["stress_level"] = footprint["occupation"] or footprint['industry']
        footprint["olfactory_profile"] = get_olfactory_profile(footprint["occupation"])
    

    return footprint




def split_job_title_and_company(job_title_and_company):
    """
    Splits a job title and company string into separate job title and company parts.
    
    :param job_title_and_company: Job title and company string to split.
    :return: Tuple containing the job title and company.
    """
    parts = re.split(SPLITTER_REGEX, job_title_and_company)
    if len(parts) == 1:
        return parts[0].strip(), None
    elif len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    else:
        return ', '.join(parts[:-1]).strip(), parts[-1].strip()
    

def extract_fingerprints_from_job_title_and_company(job_title_and_company):
    """
    Extracts any possible footprint information from a job title and company.
    
    :param job_title_and_company: Job title and company to extract information from.
    :return: Dictionary containing extracted footprint information.
    """
    footprint = {
        "job_title": None,
        "company": None,
        "olfactory_profile": None
    }

    # Split the job title and company into separate parts
    footprint["job_title"], footprint['company'] = split_job_title_and_company(job_title_and_company)
    footprint["olfactory_profile"] = get_olfactory_profile(job_title_and_company)
    return footprint   


def extract_fingerprints_from_workplace_goals(workplace_goals):
    """
    Extracts any possible footprint information from workplace goals.
    TODO: Implement a recognition of key terms in phrasing, making the spaCy model more effective.
    
    :param workplace_goals: Workplace goals to extract information from.
    :return: Dictionary containing extracted footprint information.
    """
    footprint = {
        "goals": None,
        "olfactory_profile": None
    }

    # Set the goals and olfactory profile
    footprint["goals"] = workplace_goals
    footprint["olfactory_profile"] = get_olfactory_profile(workplace_goals)
    
    return footprint




def get_notes_from_scent(scent):
    """
    Gets notes from a scent using the spaCy model.
    
    :param scent: Scent to get notes from.
    :return: List of notes associated with the scent.
    """
    db = read_json('notes.json')["fragrance-notes"]
    scent = scent.lower()
    return db.get(scent, [scent])

def get_neurotransmitter_from_scent(scent):
    """
    Gets the neurotransmitter state associated with a scent.
    
    :param scent: Scent to get the neurotransmitter state from.
    :return: Neurotransmitter state associated with the scent.
    """
    notes = get_notes_from_scent(scent)
    if not notes:
        return "N/A"
    
    # Use the first note to find the closest neurotransmitter state
    return get_all_neurotransmitter_states(notes[0], NLP_MODEL, SCENT_WORD_ASSOCIATION)[0]


def extract_fingerprints_from_favorite_scent(scent):
    """
    Extracts any possible footprint information from a favorite scent.
    
    :param scent: Favorite scent to extract information from.
    :return: Dictionary containing extracted footprint information.
    """
    footprint = {
        "scent": None,
        "notes": list(),
        "olfactory_profile": None
    }

    # Set the scent and olfactory profile
    footprint["scent"] = scent
    footprint["notes"] = get_notes_from_scent(scent)
    footprint["olfactory_profile"] = [get_neurotransmitter_from_scent(note) for note in footprint["notes"]]
    return footprint


def get_best_gender_guess(genders):
    """
    Combines gender estimates from three different sources to get the best guess as to subject gender.
    :param genders : A list of all estimates
    :return: Best guess as to subject
    """

    ans = 0
    for gender in genders:
        if "male" in gender:
            ans += 1
        elif "female" in gender:
            ans -= 1

    return ans / len(genders)



def get_nt_levels_from_fingerprints(fingerprints):
    """
    Extracts neurotransmitter levels from a list of fingerprints.
    
    :param fingerprints: List of fingerprints to extract neurotransmitter levels from.
    :return: Dictionary containing neurotransmitter levels.
    """
    nt_levels = {
        'gaba': 0,
        'dopamine': 0,
        'oxytocin': 0,
        'serotonin': 0,
        'glutamine': 0
    }
    count = 0
    
    for fingerprint in fingerprints:
        if not fingerprint:
            continue
        print(fingerprint)
        if not fingerprint:
            continue
        if 'N/A' in str(fingerprint):
            continue
        count += 1
        for nt_state, level in fingerprint:
            print(nt_state, level)
            if nt_state in nt_levels:
                nt_levels[nt_state] += level

    # Normalize the levels by the count of fingerprints
    if count > 0:
        for nt_state in nt_levels:
            nt_levels[nt_state] /= count
    
    return nt_levels

def add_email_fingerprints(data):
    """
    Adds fingerprint information extracted from email addresses to the DataFrame.
    
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with added fingerprint information.
    """
    data['fingerprint_from_email'] = data['Email Address'].apply(lambda x: extract_fingerprint_from_email(x))
    data.iloc[0]['fingerprint_from_email']  # Display the first row's fingerprint from email
    data['gender_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['gender'])
    data['age_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['age'])
    data['professional_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['professional'])
    data['occupation_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['occupation'])
    data['industry_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['industry'])
    data['stress_level_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['stress_level'])
    data['olfactory_profile_from_email'] = data['fingerprint_from_email'].apply(lambda x: x['olfactory_profile'])
    data = data.drop(columns=['fingerprint_from_email'])
    return data

def add_name_fingerprint(data):
    """
    Adds fingerprint information extracted from names to the DataFrame.
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with added fingerprint information.
    """
    data['gender_from_name'] = data['Full Name'].apply(lambda x: d.get_gender(x.split()[0]) if x else "unknown") 
    data['age_from_name'] = data['Full Name'].apply(lambda x: fake_get_age(x.split()[0]) if x else None)
    data['nationality_from_name'] = data['Full Name'].apply(lambda x: get_nationality(x.split()[-1]) if x != '' else None)
    return data

def add_job_title_and_company_fingerprints(data):
    """
    Adds fingerprint information extracted from job titles and companies, and industry, to the DataFrame.
    
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with added fingerprint information.
    """
    # Extract fingerprints from job title and company
    data['fp1'] = data['Current Job Title and Company'].apply(lambda x: extract_fingerprints_from_job_title_and_company(x))
    data['job_title'] = data['fp1'].apply(lambda x: x['job_title'])
    data['company'] = data['fp1'].apply(lambda x: x['company'])
    data['olfactory_profile_job_title'] = data['fp1'].apply(lambda x: x['olfactory_profile'])

    data['olfactory_profile_from_industry'] = data['Industry'].apply(lambda x: get_olfactory_profile(x))
    return data.drop(columns=['fp1'])


def add_workplace_goals_fingerprints(data):
    """
    Adds fingerprint information extracted from workplace goals to the DataFrame.
    
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with added fingerprint information.
    """
    # Extract fingerprints from workplace goals
    data['olfactory_profile_from_goals'] = data['Career Goals'].apply(lambda x: extract_fingerprints_from_workplace_goals(x)['olfactory_profile'])
    data['fp'] = data['Favorite Scent'].apply(lambda x: extract_fingerprints_from_favorite_scent(x))
    data['notes_from_favorite_scent'] = data['fp'].apply(lambda x: x['notes'])
    data['olfactory_profile_from_favorite_scent'] = data['fp'].apply(lambda x: x['olfactory_profile'])
    data['olfactory_profile_from_childhood_memory'] = data['Positive Childhood Scent Association'].apply(lambda x: extract_fingerprints_from_favorite_scent(x)['olfactory_profile'])
    return data.drop(columns=['fp'])

def generate_cumulative_olfactory_profile(data):
    """
    Generates a cumulative olfactory profile based on various fingerprint sources.
    
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with added cumulative olfactory profile.
    """
    # Combine all olfactory profiles into a cumulative profile
    data['olfactory_profile_cumulative'] = data.apply(
        lambda row: get_nt_levels_from_fingerprints([
            row['olfactory_profile_from_email'],
            row['olfactory_profile_job_title'],
            row['olfactory_profile_from_industry'],
            row['olfactory_profile_from_goals'],
            row['olfactory_profile_from_favorite_scent'],
            row['olfactory_profile_from_childhood_memory']
        ]), axis=1
    )

    data['dopamine_need'] = data['olfactory_profile_cumulative'].apply(lambda x: x['dopamine'])
    data['gaba_need'] = data['olfactory_profile_cumulative'].apply(lambda x: x['gaba'])
    data['oxytocin_need'] = data['olfactory_profile_cumulative'].apply(lambda x: x['oxytocin'])
    data['serotonin_need'] = data['olfactory_profile_cumulative'].apply(lambda x: x['serotonin'])
    data['glutamine_need'] = data['olfactory_profile_cumulative'].apply(lambda x: x['glutamine'])
    data = data.drop(columns=['olfactory_profile_cumulative'])
    return data


def apply_demographic_adjustments(data):
    """
    Applies demographic adjustments to the neurotransmitter levels
    :param data: DataFrame containing the CSV data.
    :return: DataFrame with adjusted neurotransmitter levels.
    """

    data["gender_guess"] = data.apply(
        lambda row: get_best_gender_guess([
            row['gender_from_email'],
            row['gender_from_name'],
            row['Sex']]), axis=1
    )

    for neurotransmitter in NEUROTRANSMITTERS:
        data[f'{neurotransmitter}_need'] = data.apply(
            lambda row: row[f'{neurotransmitter}_need'] + BASELINE_WOMEN_LEVELS.get(neurotransmitter, 0) 
            * row['gender_guess'] + BASELINE_OLD_AGE_LEVELS.get(neurotransmitter, 0) * (((50 - row['age_from_email'])/30) if isinstance(row['age_from_email'], int) else 0),
            axis=1)
        
    return data

def process_data(df):
    """
    Processes the df by adding fingerprint information and generating cumulative olfactory profiles.
    
    :param df: DataFrame containing the CSV data.
    :return: Processed DataFrame with added fingerprint information and cumulative olfactory profiles.
    """
    data = rename_columns(df)
    data = add_email_fingerprints(data)
    data = add_name_fingerprint(data)
    data = add_job_title_and_company_fingerprints(data)
    data = add_workplace_goals_fingerprints(data)
    data = generate_cumulative_olfactory_profile(data)
    data = apply_demographic_adjustments(data)
    
    return data

def process_data_from_form(post_data):
    """
    Processes the form data from a form and returns the processed DataFrame.
    
    :param file_path:  POST request containing the form data.
    :return: Processed DataFrame with added fingerprint information and cumulative olfactory profiles.
    """
    form_answers = dict()
    for key, value in post_data.items():
        if isinstance(value, list):
            form_answers[key] = ', '.join(value)
        else:
            form_answers[key] = value

    form_answers = pd.DataFrame([form_answers])
    print("DDATA: ", form_answers.head())

    return json.dumps(process_data(form_answers).iloc[0].to_dict(), indent=4)  # Convert the first row to a dictionary and return as string

