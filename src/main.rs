use rand::seq::SliceRandom;
use rand::{thread_rng, Rng};
use web_sys::HtmlInputElement;
use yew::events::SubmitEvent;
use yew::prelude::*;

struct StateCapital {
    state: &'static str,
    capital: &'static str,
}

static STATE_CAPITALS: &[StateCapital] = &[
    StateCapital { state: "Alabama", capital: "Montgomery" },
    StateCapital { state: "Alaska", capital: "Juneau" },
    StateCapital { state: "Arizona", capital: "Phoenix" },
    StateCapital { state: "Arkansas", capital: "Little Rock" },
    StateCapital { state: "California", capital: "Sacramento" },
    StateCapital { state: "Colorado", capital: "Denver" },
    StateCapital { state: "Connecticut", capital: "Hartford" },
    StateCapital { state: "Delaware", capital: "Dover" },
    StateCapital { state: "Florida", capital: "Tallahassee" },
    StateCapital { state: "Georgia", capital: "Atlanta" },
    StateCapital { state: "Hawaii", capital: "Honolulu" },
    StateCapital { state: "Idaho", capital: "Boise" },
    StateCapital { state: "Illinois", capital: "Springfield" },
    StateCapital { state: "Indiana", capital: "Indianapolis" },
    StateCapital { state: "Iowa", capital: "Des Moines" },
    StateCapital { state: "Kansas", capital: "Topeka" },
    StateCapital { state: "Kentucky", capital: "Frankfort" },
    StateCapital { state: "Louisiana", capital: "Baton Rouge" },
    StateCapital { state: "Maine", capital: "Augusta" },
    StateCapital { state: "Maryland", capital: "Annapolis" },
    StateCapital { state: "Massachusetts", capital: "Boston" },
    StateCapital { state: "Michigan", capital: "Lansing" },
    StateCapital { state: "Minnesota", capital: "Saint Paul" },
    StateCapital { state: "Mississippi", capital: "Jackson" },
    StateCapital { state: "Missouri", capital: "Jefferson City" },
    StateCapital { state: "Montana", capital: "Helena" },
    StateCapital { state: "Nebraska", capital: "Lincoln" },
    StateCapital { state: "Nevada", capital: "Carson City" },
    StateCapital { state: "New Hampshire", capital: "Concord" },
    StateCapital { state: "New Jersey", capital: "Trenton" },
    StateCapital { state: "New Mexico", capital: "Santa Fe" },
    StateCapital { state: "New York", capital: "Albany" },
    StateCapital { state: "North Carolina", capital: "Raleigh" },
    StateCapital { state: "North Dakota", capital: "Bismarck" },
    StateCapital { state: "Ohio", capital: "Columbus" },
    StateCapital { state: "Oklahoma", capital: "Oklahoma City" },
    StateCapital { state: "Oregon", capital: "Salem" },
    StateCapital { state: "Pennsylvania", capital: "Harrisburg" },
    StateCapital { state: "Rhode Island", capital: "Providence" },
    StateCapital { state: "South Carolina", capital: "Columbia" },
    StateCapital { state: "South Dakota", capital: "Pierre" },
    StateCapital { state: "Tennessee", capital: "Nashville" },
    StateCapital { state: "Texas", capital: "Austin" },
    StateCapital { state: "Utah", capital: "Salt Lake City" },
    StateCapital { state: "Vermont", capital: "Montpelier" },
    StateCapital { state: "Virginia", capital: "Richmond" },
    StateCapital { state: "Washington", capital: "Olympia" },
    StateCapital { state: "West Virginia", capital: "Charleston" },
    StateCapital { state: "Wisconsin", capital: "Madison" },
    StateCapital { state: "Wyoming", capital: "Cheyenne" },
];

#[function_component(App)]
fn app() -> Html {
    // remaining indices we can ask (we'll remove them on correct answers)
    let remaining = use_state(|| (0..STATE_CAPITALS.len()).collect::<Vec<usize>>());

    // index of the current question (into STATE_CAPITALS)
    let current_index = {
        let remaining = remaining.clone();
        use_state(move || {
            let vec = &*remaining;
            if vec.is_empty() {
                None
            } else {
                let mut rng = thread_rng();
                let &idx = vec.choose(&mut rng).unwrap();
                Some(idx)
            }
        })
    };

    let score = use_state(|| 0usize);
    let total = use_state(|| 0usize);

    // feedback icon + message + color (✔ / ✘, text, and color)
    let feedback_icon = use_state(|| "".to_string());
    let feedback_message = use_state(|| "".to_string());
    let feedback_color = use_state(|| "#111827".to_string());

    // input ref so we can read and clear the answer
    let input_ref = use_node_ref();

    // Are we finished?
    let finished = (*current_index).is_none() || (*remaining).is_empty();

    // ----- Submit handler -----
    let onsubmit = {
        let current_index = current_index.clone();
        let remaining = remaining.clone();
        let score = score.clone();
        let total = total.clone();
        let feedback_icon = feedback_icon.clone();
        let feedback_message = feedback_message.clone();
        let feedback_color = feedback_color.clone();
        let input_ref = input_ref.clone();

        Callback::from(move |e: SubmitEvent| {
            e.prevent_default();

            // If we're done, ignore further submits
            if (*current_index).is_none() {
                return;
            }

            let mut remaining_vec = (*remaining).clone();
            let mut score_val = *score;
            let mut total_val = *total;

            // Get the user's answer from the input element
            let input = match input_ref.cast::<HtmlInputElement>() {
                Some(i) => i,
                None => return,
            };

            let user_answer = input.value().trim().to_string();

            if let Some(idx) = *current_index {
                let state = STATE_CAPITALS[idx].state;
                let correct_capital = STATE_CAPITALS[idx].capital;

                total_val += 1;

                if user_answer.to_lowercase() == correct_capital.to_lowercase() {
                    // Correct
                    score_val += 1;
                    feedback_icon.set("✔".to_string());
                    feedback_message.set(format!(
                        "Correct! The capital of {} is {}.",
                        state, correct_capital
                    ));
                    feedback_color.set("#16a34a".to_string()); // green

                    // Remove this index so we don't ask again
                    remaining_vec.retain(|&i| i != idx);
                } else {
                    // Incorrect
                    feedback_icon.set("✘".to_string());
                    feedback_message.set(format!(
                        "Not quite. The capital of {} is {}.",
                        state, correct_capital
                    ));
                    feedback_color.set("#dc2626".to_string()); // red
                }

                // Update score/total
                score.set(score_val);
                total.set(total_val);

                // Clear the input box
                input.set_value("");

                // Decide next question
                if remaining_vec.is_empty() {
                    // all done!
                    remaining.set(remaining_vec);
                    current_index.set(None);
                } else {
                    let mut rng = thread_rng();
                    let next_idx = *remaining_vec
                        .choose(&mut rng)
                        .expect("non-empty remaining states");
                    remaining.set(remaining_vec);
                    current_index.set(Some(next_idx));
                }
            }
        })
    };

    // ----- Play Again handler -----
    let on_play_again = {
        let remaining = remaining.clone();
        let current_index = current_index.clone();
        let score = score.clone();
        let total = total.clone();
        let feedback_icon = feedback_icon.clone();
        let feedback_message = feedback_message.clone();
        let feedback_color = feedback_color.clone();

        Callback::from(move |_| {
            let len = STATE_CAPITALS.len();
            if len == 0 {
                return;
            }

            // Reset state
            remaining.set((0..len).collect());
            score.set(0);
            total.set(0);
            feedback_icon.set(String::new());
            feedback_message.set(String::new());
            feedback_color.set("#111827".to_string());

            // Pick a fresh random starting index
            let mut rng = thread_rng();
            let idx = rng.gen_range(0..len);
            current_index.set(Some(idx));
        })
    };

    let (state_name, prompt_text) = if let Some(idx) = *current_index {
        (
            STATE_CAPITALS[idx].state,
            "Guess the capital of this state:",
        )
    } else {
        ("All done! 🎉", "You answered all 50 state capitals correctly!")
    };

    let score_text = format!("Score: {}/{}", *score, *total);
    let finished_text = if finished && STATE_CAPITALS.len() > 0 && *score == STATE_CAPITALS.len() {
        Some("Amazing job! You got all 50 right in this session. 🎉🇺🇸".to_string())
    } else if finished {
        Some("You've answered all the states in this session!".to_string())
    } else {
        None
    };

    html! {
        <div
            style="
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                background: #1e3a8a;
            "
        >
            <div
                style="
                    background: #e0f2fe;
                    border-radius: 12px;
                    padding: 16px 20px;
                    box-shadow: 0 10px 25px rgba(15, 23, 42, 0.4);
                    max-width: 420px;
                    width: 100%;
                "
            >
                <div
                    style="
                        background: #1d4ed8;
                        color: white;
                        padding: 8px 12px;
                        border-radius: 8px;
                        font-size: 18px;
                        font-weight: 700;
                        text-align: center;
                        margin-bottom: 10px;
                    "
                >
                    { "U.S. State Capitals Quiz" }
                </div>

                <p
                    style="
                        margin: 4px 0 0 0;
                        font-size: 13px;
                        color: #0f172a;
                        text-align: center;
                    "
                >
                    { prompt_text }
                </p>

                <p
                    style="
                        margin: 6px 0 12px 0;
                        font-size: 22px;
                        font-weight: 700;
                        color: #111827;
                        text-align: center;
                    "
                >
                    { state_name }
                </p>

                <form onsubmit={onsubmit}>
                    <div style="display: flex; gap: 6px; justify-content: center;">
                        <input
                            ref={input_ref}
                            type="text"
                            placeholder="Type the capital..."
                            style="
                                flex: 1;
                                padding: 6px 8px;
                                font-size: 14px;
                                border-radius: 6px;
                                border: 1px solid #9ca3af;
                            "
                            disabled={finished}
                        />
                        <button
                            type="submit"
                            disabled={finished}
                            style="
                                padding: 6px 10px;
                                font-size: 14px;
                                font-weight: 600;
                                border-radius: 6px;
                                border: none;
                                background: #22c55e;
                                color: white;
                                cursor: pointer;
                            "
                        >
                            { "Submit" }
                        </button>
                    </div>
                </form>

                <p
                    style="
                        margin: 8px 0 4px 0;
                        font-size: 13px;
                        font-weight: 600;
                        color: #111827;
                        text-align: center;
                    "
                >
                    { score_text }
                </p>

                <div style="text-align: center; margin-top: 4px;">
                    {
                        if !(*feedback_icon).is_empty() {
                            html! {
                                <span
                                    style={format!(
                                        "display: inline-block; font-size: 20px; color: {}; margin-right: 4px;",
                                        *feedback_color
                                    )}
                                >
                                    { &*feedback_icon }
                                </span>
                            }
                        } else {
                            html! {}
                        }
                    }
                    {
                        if !(*feedback_message).is_empty() {
                            html! {
                                <span
                                    style={format!(
                                        "font-size: 13px; color: {};",
                                        *feedback_color
                                    )}
                                >
                                    { &*feedback_message }
                                </span>
                            }
                        } else {
                            html! {}
                        }
                    }
                </div>

                {
                    if let Some(done_msg) = finished_text {
                        html! {
                            <>
                                <p
                                    style="
                                        margin-top: 10px;
                                        font-size: 13px;
                                        color: #0f766e;
                                        text-align: center;
                                    "
                                >
                                    { done_msg }
                                </p>
                                <div style="text-align: center; margin-top: 8px;">
                                    <button
                                        onclick={on_play_again}
                                        style="
                                            padding: 6px 12px;
                                            font-size: 13px;
                                            font-weight: 600;
                                            border-radius: 6px;
                                            border: none;
                                            background: #2563eb;
                                            color: white;
                                            cursor: pointer;
                                        "
                                    >
                                        { "Play Again" }
                                    </button>
                                </div>
                            </>
                        }
                    } else {
                        html! {}
                    }
                }
            </div>
        </div>
    }
}

fn main() {
    yew::Renderer::<App>::new().render();
}