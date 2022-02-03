var APPOINTMENT_STATUS = {
    'pending': 1,
    'consulting': 2,
    'finished': 3,
    'cancelled': 4,
    'expired': 5
};

function changingAppointmentStatus(appointment_id, status, successCallback, errorCallback) {
    fetch('/appointment/' + appointment_id, {
        'method': 'PUT',
        headers: {
            'Content-type': 'application/json; charset=UTF-8'
        },
        'body': JSON.stringify({
            status: status
        })
    }).then(successCallback).catch(errorCallback);
}

function performConsultation(appointment_id) {
    changingAppointmentStatus(
        appointment_id,
        APPOINTMENT_STATUS.consulting,
        function (response) {
            window.location.href = '/appointment/' + appointment_id;
        },
        function (error) {
            console.error(error);
            window.location.href = '/appointment/' + appointment_id;
        }
    );
}

function finishConsultation(appointment_id) {
    changingAppointmentStatus(
        appointment_id,
        APPOINTMENT_STATUS.finished,
        function (response) {
            window.location.href = '/appointment/' + appointment_id;
        },
        function (error) {
            console.error(error);
            window.location.href = '/appointment/' + appointment_id;
        }
    );
}
