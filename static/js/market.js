async function searchMarketPrice() {

    const crop = document.getElementById("crop").value;
    const state = document.getElementById("state").value;
    const district = document.getElementById("district").value;
    const mandi = document.getElementById("mandi").value;

    const status = document.getElementById("status");
    const table = document.getElementById("price-table");

    if (!crop) {
        status.innerHTML = "⚠️ Please select a crop.";
        return;
    }

    status.innerHTML = "🔄 Searching market prices...";
    table.innerHTML = "";

    try {

        const params = new URLSearchParams({
            crop: crop,
            state: state,
            district: district,
            mandi: mandi
        });

        const response = await fetch(
            "/api/market-prices?" + params.toString()
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Unable to fetch data");
        }

        if (!data.records || data.records.length === 0) {

            table.innerHTML = `
                <tr>
                    <td colspan="9" class="empty">
                        No market data found for this search.
                    </td>
                </tr>
            `;

            status.innerHTML =
                "ℹ️ No matching mandi data available.";

            return;
        }

        data.records.forEach(record => {

            const row = document.createElement("tr");

            row.innerHTML = `
                <td>${record.commodity || "-"}</td>
                <td>${record.state || "-"}</td>
                <td>${record.district || "-"}</td>
                <td>${record.market || "-"}</td>
                <td>${record.variety || "-"}</td>
                <td>₹${record.min_price || "-"}</td>
                <td>₹${record.max_price || "-"}</td>
                <td>₹${record.modal_price || "-"}</td>
                <td>${record.date || "-"}</td>
            `;

            table.appendChild(row);
        });

        status.innerHTML =
            `✅ Found ${data.records.length} market record(s).`;

    }

    catch (error) {

        console.error(error);

        table.innerHTML = `
            <tr>
                <td colspan="9" class="empty">
                    ⚠️ Live market data is currently unavailable.
                    Please try again later.
                </td>
            </tr>
        `;

        status.innerHTML =
            "⚠️ Market data service is currently unavailable.";
    }
}