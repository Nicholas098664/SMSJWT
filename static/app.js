

function showLoader() {
    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "flex";
}

function hideLoader() {
    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "none";
}



window.register = async function () {

    showLoader();

    try {

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        const res = await fetch("/signup", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: name,
                email,
                password
            })
        });

        const data = await res.json();

        if (data.success) {
            document.getElementById("msg").innerText =
                "Registration successful! Redirecting...";

            setTimeout(() => {
                window.location.href = "/login";
            }, 1500);

        } else {
            showToast(data.message, "error");
        }

    } catch (err) {
        console.error(err);
        showToast("Unable to connect to the server.", "error");

    } finally {
        hideLoader();
    }

};



window.login = async function () {

    showLoader();

    try {

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        const res = await fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                email,
                password
            })
        });

        const data = await res.json();

        if (data.success && data.token) {

            localStorage.setItem("token", data.token);

            window.location.href = "/dashboard";

        } else {

            showToast(data.message, "error");

        }

    } catch (err) {

        console.error(err);
        showToast("Server connection failed.", "error");

    } finally {

        hideLoader();

    }

};


window.submitStudent = async function () {

    showLoader();

    try {

        const token = localStorage.getItem("token");

        const name = document.getElementById("studentName").value.trim();
        const age = document.getElementById("studentAge").value;
        const grade = document.getElementById("studentGrade").value.trim();

        const res = await fetch("http://127.0.0.1:5000/addstudent", {

            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Authorization": token
            },

            body: JSON.stringify({
                name,
                age,
                grade
            })

        });

        const data = await res.json();

        


        showToast(
            data.message,
            data.success ? "success" : "error"
        );
        console.log("Toast function executed");
        if (data.success) {

            hideAddStudent();

            loadStudents();

        }

    } catch (err) {

        console.error(err);

        showToast(
            "Failed to add student.",
            "error"
        );

    } finally {

        hideLoader();

    }

};


// SHOW / HIDE FORM


window.showAddStudent = function () {

    document.getElementById("addStudentForm").style.display = "block";

};

window.hideAddStudent = function () {

    resetForm();

};





window.loadStudents = async function () {

    showLoader();

    try {

        const token = localStorage.getItem("token");

        const res = await fetch("http://127.0.0.1:5000/Allstudents", {

            method: "GET",

            headers: {
                "Content-Type": "application/json",
                "Authorization": token
            }

        });

        const data = await res.json();

        const table = document.getElementById("studentTable");

        table.innerHTML = "";

        

        if (!data || data.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="5" style="text-align:center;">
                        No students found
                    </td>
                </tr>
            `;

            return;

        }

        data.forEach(student => {

            table.innerHTML += `
                <tr>
                    <td>${student.student_id}</td>
                    <td>${student.name}</td>
                    <td>${student.age}</td>
                    <td>${student.grade}</td>

                    <td>

                        <button onclick="editStudent('${student.student_id}')">
                            Edit
                        </button>

                        <button onclick="deleteStudent('${student.student_id}')">
                            Delete
                        </button>

                    </td>

                </tr>
            `;

        });

    } catch (err) {

        console.error(err);

        showToast(
            "Unable to load students.",
            "error"
        );

    } finally {

        hideLoader();

    }

};




window.deleteStudent = async function(student_id){

    if(!confirm("Are you sure you want to delete this student?"))
        return;

    showLoader();

    try{

        const token = localStorage.getItem("token");

        const res = await fetch(

            `http://127.0.0.1:5000/delete/${student_id}`,

            {

                method:"DELETE",

                headers:{
                    "Authorization":token
                }

            }

        );

        const data = await res.json();

        showToast(

            data.message,

            data.success ? "success" : "error"

        );

        if(data.success){

            loadStudents();

        }

    }

    catch(err){

        console.error(err);

        showToast(

            "Delete failed.",

            "error"

        );

    }

    finally{

        hideLoader();

    }

};


let currentStudentId = null;

window.editStudent = async function(student_id){

    showLoader();

    try{

        currentStudentId = student_id;

        document.getElementById("addStudentForm").style.display = "block";

        document.getElementById("formTitle").innerText =
        "Update Student";

        document.getElementById("submitBtn").style.display =
        "none";

        document.getElementById("updateBtn").style.display =
        "inline-block";

        const token = localStorage.getItem("token");

        const res = await fetch(

            `http://127.0.0.1:5000/getstudent/${student_id}`,

            {

                method:"GET",

                headers:{

                    "Authorization":token

                }

            }

        );

        const student = await res.json();

        if(!student || student.message){

            showToast(

                "Failed to load student.",

                "error"

            );

            return;

        }

        document.getElementById("studentName").value =
        student.name;

        document.getElementById("studentAge").value =
        student.age;

        document.getElementById("studentGrade").value =
        student.grade;

    }

    catch(err){

        console.error(err);

        showToast(

            "Unable to fetch student.",

            "error"

        );

    }

    finally{

        hideLoader();

    }

};






window.updateStudent = async function () {

    if (!currentStudentId) {
        showToast("No student selected.", "error");
        return;
    }

    showLoader();

    try {

        const token = localStorage.getItem("token");

        const name = document.getElementById("studentName").value.trim();
        const age = document.getElementById("studentAge").value;
        const grade = document.getElementById("studentGrade").value.trim();

        const res = await fetch(
            `http://127.0.0.1:5000/update/${currentStudentId}`,
            {
                method: "PUT",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": token
                },

                body: JSON.stringify({
                    name,
                    age,
                    grade
                })
            }
        );

        const data = await res.json();

        showToast(
            data.message,
            data.success ? "success" : "error"
        );

        if (data.success) {

            loadStudents();

            resetForm();

        }

    } catch (err) {

        console.error(err);

        showToast(
            "Unable to update student.",
            "error"
        );

    } finally {

        hideLoader();

    }

};




function resetForm() {

    document.getElementById("formTitle").innerText =
        "Add Student";

    document.getElementById("submitBtn").style.display =
        "inline-block";

    document.getElementById("updateBtn").style.display =
        "none";

    document.getElementById("studentName").value = "";

    document.getElementById("studentAge").value = "";

    document.getElementById("studentGrade").value = "";

    document.getElementById("addStudentForm").style.display =
        "none";

    currentStudentId = null;

}


window.searchStudents = function () {

    const input = document
        .getElementById("searchInput")
        .value
        .toLowerCase();

    const rows =
        document.querySelectorAll("#studentTable tr");

    rows.forEach(row => {

        const nameCell = row.cells[1];

        if (!nameCell) return;

        const name =
            nameCell.textContent.toLowerCase();

        row.style.display =
            name.includes(input) ? "" : "none";

    });

};



window.loadCounter = async function () {
    try {
        const token = localStorage.getItem("token");

        const res = await fetch("http://127.0.0.1:5000/counter", {
            headers: {
                "Authorization": token
            }
        });

        

        const data = await res.json();
        console.log("Counter API:", data);

        document.getElementById("totalStudents").innerText =
            data.totalStudent;

        console.log(
            "After setting:",
             document.getElementById("totalStudents").innerText
        );    

    } catch (err) {
        console.error(err);
    }
};


window.onload = function () {

    const path = window.location.pathname;

    const token = localStorage.getItem("token");

    
    if (path.includes("dashboard")) {

        if (!token) {
            window.location.href = "/login";
            return;
        }

        loadStudents();
        loadCounter();
    }


    if (path.includes("login")) {


        if (token) {
            window.location.href = "/dashboard";
        }

    }


    if (path.includes("register")) {

        // optional: same logic if needed
        if (token) {
            window.location.href = "/dashboard";
        }
    }
};


 
 

function showToast(message, type = "success") {

    const toast = document.getElementById("toast");

    if (!toast) {
        alert(message);   // fallback
        return;
    }

    toast.innerText = message;
    toast.className = "toast " + type;
    toast.style.display = "block";

    setTimeout(() => {
        toast.style.display = "none";
    }, 3000);

}



window.logout = function () {

    const confirmLogout = confirm("Are you sure you want to logout?");

    if (!confirmLogout) return;

    // remove token
    localStorage.removeItem("token");

    // clear login inputs (important)
    const email = document.getElementById("email");
    const password = document.getElementById("password");

    if (email) email.value = "";
    if (password) password.value = "";

    showToast("Logged out successfully.", "success");

    setTimeout(() => {
        window.location.href = "/login";
    }, 800);
};





window.togglePassword = function () {

    const passwordInput = document.getElementById("password");
    const toggleIcon = document.querySelector(".toggle-eye");

    if (!passwordInput || !toggleIcon) return;

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        toggleIcon.textContent = "🙈";
    } else {
        passwordInput.type = "password";
        toggleIcon.textContent = "👁";
    }
};






