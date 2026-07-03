window.onload = function () {
    loadAudit();
};

async function loadAudit() {
    try {
        const token = localStorage.getItem("token");

        const res = await fetch("http://127.0.0.1:5000/audit_logs", {
            method: "GET",
            headers: {
                "Authorization": `Bearer ${token}`
            }
        });

        const data = await res.json();

        if (!res.ok) {
            console.log(data);
            return;
        }

        const body = document.getElementById("auditBody");
        body.innerHTML = "";

        data.forEach(log => {
            body.innerHTML += `
                <tr>
                    <td>${log.id}</td>
                    <td>${log.user}</td>
                    <td>${log.action}</td>
                    <td>${log.time}</td>
                </tr>
            `;
        });

    } catch (err) {
        console.log("Audit load error:", err);
    }
}