var APPOINTMENT_STATUS = {
    'pending': 1,
    'consulting': 2,
    'finished': 3,
    'cancelled': 4,
    'expired': 5
};

var PRESCRIPTION_TYPE = {
    'standard': 's',
    'repeatable': 'r'
};

function changingAppointmentStatus(appointment_id, status, successCallback, errorCallback) {
    fetch('/appointment/' + appointment_id, {
        'method': 'PUT',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8'
        },
        'body': JSON.stringify({
            'status': status
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

function makeRepeatable(patient_id, prescription_id) {
    fetch('/prescription/' + prescription_id + '/type', {
        'method': 'PUT',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8'
        },
        'body': JSON.stringify({
            'patient_id': patient_id,
            'type': PRESCRIPTION_TYPE.repeatable
        })
    }).then(function (response) {
        window.location.href = '/patient/' + patient_id;
    }).catch(function (error) {
        console.error(error);
        window.location.href = '/patient/' + patient_id;
    });
}

function cancelAppointment(appointment_id) {
    fetch('/appointment/' + appointment_id, {
        'method': 'PUT',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8'
        },
        'body': JSON.stringify({
            'status': APPOINTMENT_STATUS.cancelled
        })
    }).then(function (response) {
        window.location.href = '/appointment/' + appointment_id;
    }).catch(function (error) {
        console.error(error);
        window.location.href = '/appointment/' + appointment_id;
    });
}

function cancelPatientAppointment(patient_id, appointment_id) {
    fetch('/appointment/' + appointment_id, {
        'method': 'PUT',
        'headers': {
            'Content-type': 'application/json; charset=UTF-8'
        },
        'body': JSON.stringify({
            'patient_id': patient_id,
            'status': APPOINTMENT_STATUS.cancelled
        })
    }).then(function (response) {
        window.location.href = '/patient/' + patient_id;
    }).catch(function (error) {
        console.error(error);
        window.location.href = '/patient/' + patient_id;
    });
}
