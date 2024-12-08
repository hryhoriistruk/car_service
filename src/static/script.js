function showButtons(shift) {
    const buttonsContainer = shift.querySelector('.shift-buttons');
    if (buttonsContainer) {
        buttonsContainer.style.display = 'block';
    }
}


function hideButtons(shift) {
    shift.querySelector('.shift-buttons').style.display = 'none';
}

// Add a global variable to store the current shift ID being edited
let currentShiftId;

function editShift(shiftId) {
    // Set the currentShiftId variable
    currentShiftId = shiftId;

    // Construct the ID for the working hours container
    const workingHoursId = `working-hours-${shiftId}`;

    // Get the working hours container element using its ID
    const workingHoursContainer = document.getElementById(workingHoursId);

    if (workingHoursContainer) {
        // Extract text content from the working hours container
        const workingHoursText = workingHoursContainer.innerText;

        // Use a regular expression to extract hours and minutes
        const timeRegex = /(\d{2}):(\d{2}) - (\d{2}):(\d{2})/;
        const match = workingHoursText.match(timeRegex);

        if (match) {
            // Extracted hours and minutes
            const startHour = match[1];
            const startMinute = match[2];
            const endHour = match[3];
            const endMinute = match[4];

            // Populate the modal form with the extracted start time and end time
            document.getElementById('startTime').value = `${startHour}:${startMinute}`;
            document.getElementById('endTime').value = `${endHour}:${endMinute}`;

            // Show the modal
            document.getElementById('editModal').style.display = 'block';
        } else {
            console.error('Unable to parse hours and minutes from working hours text.');
        }
    } else {
        console.error(`Working hours container not found with ID ${workingHoursId}.`);
    }
}


function applyEdit() {
    // Get values from the form
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;

    // Prepare data for the PUT request
    const formData = new FormData();
    formData.append('start_time', startTime);
    formData.append('end_time', endTime);

    // Send the PUT request to update the shift
    fetch(`/shifts/${currentShiftId}`, {
        method: 'PUT',
        body: formData,
    })
        .then(response => {
            if (response.ok) {
                // If the update is successful, close the modal and update the shift
                closeModal();
                updateShift(currentShiftId);
            } else {
                // Handle error scenarios as needed
                console.error('Failed to update shift:', response.statusText);
            }
        })
        .catch(error => {
            console.error('Error updating shift:', error);
        });
}

function updateShift(shiftId) {
    // Implement logic to update the content of the corresponding shift div
    // You can use fetch or other methods to retrieve updated shift data from the server
    // and then update the HTML content of the shift div
    console.log(`Updating shift with ID ${shiftId}`);
}

// Rest of your existing code...


function closeModal() {
    document.getElementById('editModal').style.display = 'none';
}


function deleteShift(shiftId) {
    // Implement your delete logic here
    alert('Deleting shift with ID ' + shiftId);
}