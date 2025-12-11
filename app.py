import gradio as gr

def generate_array_html(arr, low, high, mid, target_found=False):
    """
    This function shows makes the demonstration arrays the user will see
    
    Takes the current state of the algorithm (low, high, mid pointers)
    and returns a string of HTML that draws a row of boxes.
    - Green = Found target
    - Yellow = Current midpoint
    - Blue = Active search range
    - Gray = Inactive numbers
    """
    # Align items in a row
    html_content = '<div style="display: flex; gap: 5px; font-family: monospace; font-size: 20px;">'

    # Make box for every number
    for i, num in enumerate(arr):
        # Default/inactive number
        bg_color = "#e0e0e0"
        text_color = "#a0a0a0"
        border = "1px solid #ccc"

        # Colour the boxes
        if i == mid and target_found:
            bg_color = "#4CAF50" # Found. This is green.
            text_color = "white"
        elif i == mid:
            bg_color = "#FFEB3B" # Midpoint. This is yellow.
            text_color = "black"
            border = "2px solid orange"
        elif low <= i <= high:
            bg_color = "#E3F2FD" # Active range. This is blue.
            text_color = "black"
            border = "1px solid #2196F3"

        # CSS
        box_style = (
            f"background-color: {bg_color}; "
            f"color: {text_color}; "
            f"padding: 10px; "
            f"border-radius: 5px; " # Rounded corners
            f"border: {border}; "
            f"width: 40px; "
            f"text-align: center;"
        )
        
        # Add this box to the HTML string
        html_content += f'<div style="{box_style}">{num}</div>'

    # Close container div
    html_content += "</div>"
    return html_content

def binary_search_step_by_step(user_list_input, user_target_input):
    """
    The main logic function. It performs Binary Search and records every step 
    visually so the user can see the history.
    """
    try:
        # Check if input is empty
        if not user_list_input.strip():
            return "<div>Please enter a list.</div>", "Waiting for input..."

        # Parse input into list
        number_list = [int(x.strip()) for x in user_list_input.split(',')]
        target = int(user_target_input)
    except ValueError:
        # Inform user if they typed text rather than numbers
        return "<div style='color:red'>Error: Invalid input. Use numbers separated by commas.</div>", "Error"

    # Binary search needs a sorted list, so sort the list
    number_list.sort()
    
    # Initialize pointers
    low = 0
    high = len(number_list) - 1

    # Store all HML strings to display at once.
    full_html_log = ""

    step_count = 1
    # Show initial (sorte) list
    full_html_log += f"<h3>Sorted List: {number_list} | Target: {target}</h3><hr>"

    # Binary search
    while low <= high:
        # Get mid
        mid = (low + high) // 2
        mid_value = number_list[mid]

        # Create visual of array fro current step
        step_visual = generate_array_html(number_list, low, high, mid, target_found=(mid_value == target))

        # Explain current step with text
        explanation = f"<strong>Step {step_count}:</strong> Checking index {mid} (Value: {mid_value})."
        
        # Explain why we move left or right.
        if mid_value < target:
            explanation += f" {mid_value} < target value ({target}). We need to search higher values"
        elif mid_value > target:
            explanation += f" {mid_value} > target value ({target}). We need to search higher values"

        # Append explanation to full log.
        full_html_log += f"<div style='margin-bottom: 20px;'>{explanation}<br>{step_visual}</div>"

        # Comparisons
        if mid_value == target:
            # Add success message and return full log if found.
            full_html_log += f"<h3 style='color: green;'>Match Found at Index {mid}!</h3>"
            return full_html_log, f"Success: Found {target} at index {mid}"
        # otherwise do more binary search.
        elif mid_value < target:
            low = mid + 1
        else:
            high = mid - 1

        step_count += 1

    # If loop finishes without returning, target was not found.
    full_html_log += "<h3 style='color: red;'>Target Not Found.</h3>"
    return full_html_log, f"Target {target} not found."

# Gradio things
with gr.Blocks() as demo:
    gr.Markdown("# Binary Search Visualizer")
    gr.Markdown("Enter a list of numbers and a target. The app will generate a visual for the search.")

    # Row to hold inputs and the button
    with gr.Row():
        list_input = gr.Textbox(label="List (e.g., 1, 5, 8, 12, 20)", value="1, 5, 8, 12, 20, 35, 42, 55, 60")
        target_input = gr.Textbox(label="Target", value="42")
        btn = gr.Button("Search", variant="primary")

    # Outputs
    # We use gr.HTML instead of gr.Textbox because colours help the visual
    visual_output = gr.HTML(label="Visual Execution Log")
    result_text = gr.Label(label="Final Result")

    # Make the button act like a button.
    btn.click(binary_search_step_by_step, inputs=[list_input, target_input], outputs=[visual_output, result_text])

# Let us, with all due respect (and consideration for the feelings of the program), kindly allow the application to commence if it so pleases.
if __name__ == "__main__":
    demo.launch(share=True)