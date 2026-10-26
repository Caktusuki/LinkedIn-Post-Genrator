from llm_helper import llm
from influencer_posts import select_influencer_posts


def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"


def generate_post(length, language, tag, influencer):
    prompt = get_prompt(length, language, tag, influencer)
    response = llm.invoke(prompt)
    return response.content


def get_prompt(length, language, tag, influencer):
    length_str = get_length_str(length)

    selected = select_influencer_posts(influencer, tag, length, language)
    role = selected["role"]
    style_notes = selected["style_notes"]
    examples = selected["posts"]

    prompt = f'''
    Generate a new, original LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English.
    The script for the generated post should always be English.

    4) Write in the voice and style of {influencer} ({role}).
    Style notes: {style_notes}
    '''

    if len(examples) > 0:
        prompt += "5) The following example posts show the influencer's writing style. Match that voice and tone, but write an entirely NEW post — do not copy, quote, or reuse the example content."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

    return prompt


if __name__ == "__main__":
    print(generate_post("Medium", "English", "Career", "Rohan Mehta"))