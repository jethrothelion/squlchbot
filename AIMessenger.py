from llama_cpp import Llama

context = []
model = Llama.from_pretrained(
    repo_id="OBLITERATUS/gemma-4-E4B-it-OBLITERATED",
    filename="gemma-4-E4B-it-OBLITERATED-Q5_K_M.gguf",
    n_gpu_layers=-1,
    n_ctx=2048,
    verbose=False
)

def add_message(message, user = "", role = "user"):
    print(message, user)
    if role == "user":
        full_message = f"USER: {user}. MESSAGE: {message}"
    else:
        full_message = message
    context.append({"role": role, "content": full_message})


def run_model():
    outputs = model.create_chat_completion(
        messages=context,
        max_tokens=500,
        temperature=0.7,
        top_p=0.9,
        top_k=40,
        repeat_penalty=1.1
    )
    output = outputs["choices"][0]["message"]["content"]
    add_message(output, role="assistant" )
    return (output)


if __name__ == "__main__":
    username = "username"
    print(f"Chat started with {username}. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        add_message(user_input, username)

        response = run_model()
        print(f"Bot: {response}\n")
