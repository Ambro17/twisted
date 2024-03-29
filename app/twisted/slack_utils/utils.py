def create_body(body):
    return	{
        "type": "input",
        'block_id': 'block_body',
        "label": {
            "type": "plain_text",
            "text": "Body",
        },
        "element": {
            "type": "plain_text_input",
            "multiline": True,
            "action_id": "thread_description_action_id",
            "initial_value": body,
        },
    }

def create_title(title):
    if len(title) > 100:
        title = f'{title[:100]}...'
    return {
        "type": "input",
        'block_id': 'block_title',
        "label": {
            "type": "plain_text",
            "text": "Title",

        },
        "element": {
            "type": "plain_text_input",
            "initial_value": title,
            "action_id": "thread_title_action_id"
        },
    }


def create_modal(title, body, action_id, channel_id, message_timestamp, message_permalink):
	NEW_THREAD_MODAL = {
		"type": "modal",
        "callback_id": action_id,
		"title":  {"type": "plain_text", "text": "Hero"},
		"submit": {"type": "plain_text", "text": "Submit"},
		"close":  {"type": "plain_text", "text": "Cancel"},
		"blocks": [
			{
				"type": "section",
				"text": {
					"type": "plain_text",
					"text": "Customize the title and body of the new thread from here",
				}
			},
			create_title(title),
			create_body(body)
		],
        "private_metadata": f"{channel_id}|{message_timestamp}|{message_permalink}"
	}
	return NEW_THREAD_MODAL
    

def link(text: str, link: str) -> str:
    return f"<{link}|{text}>"
