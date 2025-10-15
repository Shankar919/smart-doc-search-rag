import os
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

PROMPT = """You are an assistant that answers user questions using ONLY the provided context snippets.
If the answer can't be found in the snippets, say "I don't know."\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer succinctly and cite snippet ids you used, like: (source: <id>)\n"""

def format_context(snippets):
    lines = []
    for s in snippets:
        sid = getattr(s, 'id', None) or s.get('id')
        payload = getattr(s, 'payload', None) or s.get('payload', {})
        text = payload.get('text','') if isinstance(payload, dict) else (payload or '')
        lines.append(f"[{sid}] {text}")
    return "\n\n".join(lines)

def synthesize_answer(question, snippets):
    context = format_context(snippets)
    prompt = PROMPT.format(context=context, question=question)
    if OPENAI_KEY:
        import openai
        openai.api_key = OPENAI_KEY
        resp = openai.ChatCompletion.create(
            model='gpt-4o-mini',
            messages=[{'role':'user','content':prompt}],
            temperature=0.0,
            max_tokens=400
        )
        return resp['choices'][0]['message']['content'].strip()
    else:
        # fallback: concatenate snippets
        combined = '\n\n'.join([ (s.get('payload') or {}).get('text','') for s in snippets ])
        return combined[:800]
