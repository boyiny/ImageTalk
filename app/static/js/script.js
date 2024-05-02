document.addEventListener('DOMContentLoaded', function() {
    const extract_info_Button = document.getElementById('extract_info_Button');
    const generate_story_Button = document.getElementById('generate_story_Button');
    const read_story_Button = document.getElementById('read_story_Button');
    const clear_all_steering_Button = document.getElementById('clear_all_steering_Button');
    const clear_all_story_Button = document.getElementById('clear_all_story_Button');
    const album = document.getElementById('album');

    // var fs = require('fs');
    // var imageFiles = fs.readdirSync('static/images');

    const imagesFolder = 'static/images';
    const imageFiles = ['pu1_1_sea.jpeg', 'pu1_2_sea.jpeg', 'pu1_3_coconut.jpeg', 'pu1_4_sea.jpeg', 'eu1_1_sunset.jpeg', 'eu1_2_dinner.jpeg', 'eu1_3_study.png', 'pu2_1_tea.jpeg', 'pu5_1_house.jpeg', 'pu7_1_mall.jpeg', 'pu7_2_mall.jpeg', 'pu7_3_slide.jpeg'];
    // console.log('imageFiles:');
    // console.log(imageFiles);

    // Selecting Images
    imageFiles.forEach(function(filename) {
        // Create a container div for each image
        const container = document.createElement('div');
        container.classList.add('image-container');

        // Create an image element for each image
        const imageElement = document.createElement('img');
        imageElement.src = `${imagesFolder}/${filename}`;
        imageElement.alt = filename;

        // Create a checkbox element for each image
        const checkboxElement = document.createElement('input');
        checkboxElement.type = 'checkbox';
        checkboxElement.classList.add('image-checkbox');

        // Create a checkmark icon for indicating selection
        const checkmarkElement = document.createElement('span');
        checkmarkElement.classList.add('checkmark');

        // Append the checkbox and checkmark elements to the container
        container.appendChild(imageElement);
        container.appendChild(checkboxElement);
        container.appendChild(checkmarkElement);

        // Append the container to the album area
        album.appendChild(container);

        // Add event listner to toggle checkmark visability
        checkboxElement.addEventListener('change', function() {
            checkmarkElement.style.display = checkboxElement.checked ? 'block' : 'none';
        });
    });
    
    // Clear all selected images


    // Processing Image
    extract_info_Button.addEventListener('click', function() {

        // Get the selected image file
        const selectedCheckboxes = document.querySelectorAll('.image-checkbox:checked');
        const imagePaths = [];

        // console.log(selectedCheckboxes);

        selectedCheckboxes.forEach(function(checkbox) {
            const image = checkbox.parentNode.querySelector('img');
            const src = image.getAttribute('src');
            imagePaths.push(src);
        });
        // console.log(imagePaths);

        // Send image data to the server for recognition
        fetch('/recognize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imagePaths: imagePaths })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }) // Parse the JSON response
        .then(data => {

            let objs = '';
            let capt = '';
            let keywords = '';

            const objRecContainer = document.getElementById('objectsOutput');
            const captionContainer = document.getElementById('captionsOutput');
            const keywordContainer = document.getElementById('keywordsInput');

            for (let i = 0; i < data.length; i++) {
                objs = objs + `Image${i+1}: ` + data[i].detected_objects.toString() + '\n';
                capt = capt + `Image${i+1}: ` + data[i].caption.toString() + '\n';  
                keywords = keywords + `Image${i+1}: ` + '\n';
            }
            objRecContainer.textContent = objs;
            captionContainer.textContent = capt; 
            keywordContainer.textContent = keywords;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Generating Story
    generate_story_Button.addEventListener('click', function() {
        const storyMaterial = {};
        const objectsContainer = document.getElementById('objectsOutput');
        const captionsContainer = document.getElementById('captionsOutput');
        const keywordsContainer = document.getElementById('keywordsInput');
        const languageStyleContainer = document.getElementById('languageInput');

        storyMaterial.objects = objectsContainer.value;
        storyMaterial.captions = captionsContainer.value;
        storyMaterial.keywords = keywordsContainer.value;
        storyMaterial.languageStyle = languageStyleContainer.value;

        // Send image data to the server for story generation
        fetch('/generate_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ languageMaterial: storyMaterial })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }) // Parse the JSON response
        .then(genterated_story => {
            // console.log('Data type:'+typeof(genterated_story));
            // console.log(genterated_story);

            const storyContainer = document.getElementById('storyOutput');
            storyContainer.textContent = genterated_story;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Clear all steering
    clear_all_steering_Button.addEventListener('click', function() {
        const objectsContainer = document.getElementById('objectsOutput').value = "";
        const captionsContainer = document.getElementById('captionsOutput').value = "";
        const keywordsContainer = document.getElementById('keywordsInput').value = "";
        const languageStyleContainer = document.getElementById('languageInput').value = "";

        // objectsContainer.textContent = '';
        // captionsContainer.textContent = '';
        // keywordsContainer.textContent = '';
        // languageStyleContainer.textContent = '';
    });

    // Read Story
    read_story_Button.addEventListener('click', function() {
        const storyContainer = document.getElementById('storyOutput');
        const story = storyContainer.textContent;

        console.log('Story: ' + story);

        // Send image data to the server for story generation
        fetch('/read_story', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ story: story })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        }) // Parse the JSON response
        .then(data => {
            console.log('Data type:'+typeof(data));
            console.log(data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Clear all story
    clear_all_story_Button.addEventListener('click', function() {
        const storyContainer = document.getElementById('storyOutput').value = "";
        
        const objectsContainer = document.getElementById('objectsOutput').value = "";
        const captionsContainer = document.getElementById('captionsOutput').value = "";
        const keywordsContainer = document.getElementById('keywordsInput').value = "";
        const languageStyleContainer = document.getElementById('languageInput').value = "";
        
        // storyContainer.textContent = '';

        // objectsContainer.textContent = '';
        // captionsContainer.textContent = '';
        // keywordsContainer.textContent = '';
        // languageStyleContainer.textContent = '';
    });

});
