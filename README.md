# Broken Window Hackathon #1
### Hosted by FutureLondon.org:
"[Future London](https://futurelondon.org/) is a community of high-agency techno-optimists. We believe that the UK is broken. But it doesn't have to be."

---


## "I Love My Neighbourhood" - How AI Can Empower a Community

Created by:  
[Mark Hodierne, @mhodierne1402](https://github.com/mhodierne1402)  
[Kailash Balasubramaniyam, @kailash19961996](https://github.com/kailash19961996)

### Background

> In criminology, the broken windows theory states that visible signs of crime, antisocial behavior, and civil disorder create an urban environment that encourages further crime and disorder, including serious crimes. The theory suggests that policing methods that target minor crimes, such as vandalism, loitering, public drinking, and fare evasion, help to create an atmosphere of order and lawfulness. The theory was introduced in a 1982 article by social scientists James Q. Wilson and George L. Kelling. It was popularized in the 1990s by New York City police commissioner William Bratton and mayor Rudy Giuliani, whose policing policies were influenced by the theory. (Wikipedia)

### Overview

"I Love My Neighbourhood" is a simple app designed to engage community members, public services and policymakers in addressing key urban challenges: 
- Enhancing urban aesthetics
- Improving community health and well-being
- Promoting sustainability in urban environments
- Ensuring safety in public spaces
- Reducing crime and anti-social behaviour

This demonstration product was developed during a hackathon organized by [Future London](https://futurelondon.org/) with contributions from policymakers and tech enthusiasts. Ultimately, the app would be deployed on mobile devices, either as a stand-alone app or as an AI bot for existing WhatsApp community groups.

Users are able to submit photos and/or comments about their local neighbourhood - things they love, like green spaces, public buildings, and community activities - and things they don't love, like graffiti, fly tipping, and broken windows. AI is leveraged to classify and analyze these reports - and track how things are changing over time. 

Such data provides insights about local urban issues, and empowers residents to work effectively with public services and voluntary bodies to make improvements. The data also helps policymakers to see the bigger picture, helping them decide which problems are critical, and allocate resources accordingly.This is Broken Window Theory in action ... grass roots fashion.

[Click here to try the app](https://broken-window-hackathon-lyjk4hpgpyrweczmewadtk.streamlit.app/)

or scan the QR code
<img width="200" alt="QR Code" src="https://github.com/mhodierne1402/broken-window-hackathon/blob/main/assets/qr_code.png">

### Architecture

![App Architecture](https://github.com/mhodierne1402/broken-window-hackathon/blob/main/assets/architecture.png)

A number of apps for mapping and reporting street problems have already been created, such as [FixMyStreet](https://www.fixmystreet.com/). UK councils have also developed their own neighbourhood reporting apps, such as [Lewes and Eastbourne councils' "Report It"](https://www.lewes-eastbourne.gov.uk/report-it) smartphone app, a customized version of the [Love Clean Streets](https://lovecleanstreets.info/) environmental reporting service.

Although such apps have demonstrated some success, they are somewhat limited in that they are simply one-way reporting channels for local residents. "I Love My Neighbourhood" demonstrates that this data, together with the capabilities of AI, can help to empower a local residents to actively monitor and improve their neighbourhoods. 

The app utilizes on two AI models to enhance its functionality:

1. **Classification Model**: Automatically categorizes user reports into predefined categories (e.g., Graffiti, Garbage, Broken Windows, Green Spaces, Public Buildings, Community Events). We have used OpenAI's ClIP Model ([clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32)) for this classification task.

2. **Summarization Model**: Generates concise summaries of user reports for each predefined category. These are especially useful when dealing with a large volume of reports. We have used OpenAI's ChatGPT-4o Large Language Model to summarize major concerns reported across the different reporting categories.

Within the scope of this hackathon, we have implemented a relatively simple AI-enhanced reporting app. A full investigation into how AI could support local communities would likely uncover many more opportunities to extend the functionality of this type of app.

### Usage

1. **Home Page**: Users can upload images and comments about urban issues they encounter and see them updated in real-time on interactive maps, which are also visible to other users.
![Screenshot 2024-07-02 at 1 28 02 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/3e19918a-8531-4cc9-8c6a-86be49965f80)
![Screenshot 2024-07-02 at 1 28 42 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/dc3bd5ab-2d8d-45ba-827e-45fa5259b478)
![Screenshot 2024-07-02 at 1 29 18 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/def7ef54-58e3-40da-a4ae-16394c7317d2)

2. **Reports**: Provides graphical representations of issue trends over time, helping track progress and hold authorities accountable.
![Screenshot 2024-07-02 at 12 13 48 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/489f52aa-22e4-4c00-a5d9-dfeb24cb38f2)

3. **Interactive Maps**: Real-time visualization of reported issues, allowing users and policymakers to see what's happening in their area.
![Screenshot 2024-07-02 at 12 13 58 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/ff492c99-866f-4a41-b5f6-1074a9bc4695)

4. **Summary Page**: AI-generated summaries of user comments for each category of urban issues.
![Screenshot 2024-07-02 at 12 14 32 AM](https://github.com/kailash19961996/Neighbourhood-app/assets/123597753/b4c91ddb-5cde-43f7-be4b-a67716812667)

## Install

**To deploy the app locally:**
1. Fork or clone this repository.
2. In the terminal, run: 
    ```pip install -r requirements.txt```
3. Create a local .env file that contains your OpenAI API key:
    ```# API key for OpenAI services
    OPENAI_API_KEY=add-your-openai-api-key-here``` 
4. Run the following command in the terminal to open the app in a new tab in your default browser:
    ```streamlit run home.py```

**To deploy the app on Streamlit:**
1. Fork or clone this repository.
2. Login to [Streamlit Hub](https://share.streamlit.io/).
3. Click `Create app` and complete the details to deploy from your GitHub repository. Specify Branch as `master` and Main file path as `hello.py`
4. Click `Advanced settings...` and enter your OpenAI API key: 
    ```OPENAI_API_KEY=add-your-openai-api-key-here```
5. Click `Deploy!`

## License
[MIT License](LICENSE). Copyright (c) 2024 Mark Hodierne, Kailash Balasubramaniyam.
