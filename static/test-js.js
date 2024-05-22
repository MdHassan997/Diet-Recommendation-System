document.addEventListener('DOMContentLoaded', () => {
    const categoryContainer = document.getElementById('categoryContainer');
    const foodList = document.getElementById('foodList');
    let categories = [];
    let subtractedItems = new Set(); // Define subtractedItems globally
    let subtractedCalories = new Map(); // Store subtracted calories for pie chart

    // Fetch data from data.json in the static folder
    fetch('/static/data.json')  // Update the path to your data.json file
        .then(response => response.json())
        .then(data => {
            // Extract unique category names
            categories = [...new Set(data.map(item => item.FoodCategory))];

            // Create buttons for each category
            categories.forEach(category => {
                const button = document.createElement('button');
                button.textContent = category;
                button.className = 'category-button';
                button.addEventListener('click', () => {
                    // Filter food list by category
                    const filteredFood = data.filter(item => item.FoodCategory === category);
                    // Display filtered food list
                    displayFoodList(filteredFood);
                });
                categoryContainer.appendChild(button);
            });
        })
        .catch(error => console.error('Error fetching data:', error));

    function displayFoodList(foodArray) {
        // Clear previous food list
        foodList.innerHTML = '';
        // Populate food list
        foodArray.forEach(item => {
            const listItem = document.createElement('li');
            listItem.className = 'food-item';
            listItem.textContent = `${item.FoodItem} (${item.FoodCategory}) - ${item.Cals_per100grams} cal`;
            foodList.appendChild(listItem);
        });
    }

    const subtractCaloriesBtn = document.getElementById('subtractCaloriesBtn');
    const totalCalorieElement = document.getElementById('totalCalorie');
    const subtractedFoodList = document.getElementById('subtractedFoodList');
    const subtractedFoodListContainer = document.getElementById('subtractedFoodListContainer');
    const showSubtractedListBtn = document.getElementById('showSubtractedListBtn');

    // Retrieve total calorie requirement from Flask route
    let totalCalorie = parseInt(totalCalorieElement.textContent);

    // Event listener for subtracting calories
    subtractCaloriesBtn.addEventListener('click', () => {
        const selectedItems = document.querySelectorAll('.food-item.selected');

        selectedItems.forEach(item => {
            const calorieText = item.textContent.split('-')[1].trim().split(' ')[0];
            const foodName = item.textContent.split('-')[0].trim();
            const calories = parseInt(calorieText);

            // Check if the item has already been subtracted
            if (!subtractedItems.has(foodName)) {
                totalCalorie -= calories; // Subtract the calories from the total calorie requirement
                item.style.textDecoration = 'line-through';
                subtractedItems.add(foodName); // Add the subtracted item to the Set

                // Store subtracted calories for pie chart
                subtractedCalories.set(foodName, calories);
            }
        });

        totalCalorieElement.textContent = totalCalorie;

        if (totalCalorie <= 0) {
            alert('Your limit calorie has been reached!');
        }

        // Show the button to reveal the subtracted list
        showSubtractedListBtn.style.display = 'inline-block';

        // Update pie chart
        updatePieChart();
    });

    // Event listener for selecting items
    foodList.addEventListener('click', (event) => {
        const listItem = event.target;
        if (listItem.tagName === 'LI') {
            listItem.classList.toggle('selected');
        }
    });

    // Event listener for showing the subtracted list
    showSubtractedListBtn.addEventListener('click', () => {
        subtractedFoodListContainer.style.display = 'block';
        showSubtractedListBtn.style.display = 'none'; // Hide the button after revealing the list

        // Display the subtracted items
        subtractedFoodList.innerHTML = Array.from(subtractedItems).map(foodName => `<div>${foodName}</div>`).join('');

        // Show the download PDF button
       
    });
    

    // Add event listener to the download PDF button
    function downloadPdf() {
        const doc = new jsPDF();
        const subtractedFoodListItems = Array.from(subtractedItems);
        // Add each subtracted food item to the PDF
        subtractedFoodListItems.forEach((foodName, index) => {
            doc.text(10, 10 + index * 10, foodName);
        });
        // Save the PDF
        doc.save('subtracted_food_list.pdf');
    }

    // Attach event listener to the download PDF button
    const downloadPdfBtn = document.getElementById('downloadPdfBtn');
    downloadPdfBtn.addEventListener('click', downloadPdf);
   

    // Function to update the pie chart
    function updatePieChart() {
        const canvas = document.getElementById('caloriesPieChart');
        const ctx = canvas.getContext('2d');

        // Clear the previous chart
        if (window.pieChart) {
            window.pieChart.destroy();
        }

        // Prepare data for the pie chart
        const labels = Array.from(subtractedItems);
        const data = labels.map(foodName => subtractedCalories.get(foodName));

        // Create new pie chart
        window.pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Subtracted Calories',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(255, 99, 132, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Subtracted Calories'
                }
            }
        });
    }
    function updatePieChart() {
        const canvas = document.getElementById('caloriesPieChart');
        const ctx = canvas.getContext('2d');

        // Clear the previous chart
        if (window.pieChart) {
            window.pieChart.destroy();
        }

        // Prepare data for the pie chart
        const labels = Array.from(subtractedItems);
        const data = labels.map(foodName => subtractedCalories.get(foodName));

        // Create new pie chart with custom options
        window.pieChart = new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Subtracted Calories',
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.7)',
                        'rgba(54, 162, 235, 0.7)',
                        'rgba(255, 206, 86, 0.7)',
                        'rgba(75, 192, 192, 0.7)',
                        'rgba(153, 102, 255, 0.7)',
                        'rgba(255, 159, 64, 0.7)',
                        'rgba(255, 99, 132, 0.7)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)',
                        'rgba(255, 99, 132, 1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                title: {
                    display: true,
                    text: 'Subtracted Calories',
                    fontSize: 20
                },
                animation: {
                    animateRotate: true, // Enable rotation animation
                    animateScale: true, // Enable scale animation
                    duration: 1500 // Animation duration in milliseconds
                },
                plugins: {
                    legend: {
                        labels: {
                            font: {
                                size: 16 // Adjust legend font size
                            }
                        }
                    }
                }
            }
        });
    }

    // Call the function to initially update the pie chart
    updatePieChart();
});

document.getElementById('showSubtractedListBtn').addEventListener('click', function() {
    // Scroll to the bottom of the page
    window.scrollTo(0, document.body.scrollHeight);
});