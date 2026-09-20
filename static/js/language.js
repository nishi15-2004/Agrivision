document.addEventListener("DOMContentLoaded", async function () {

    const languageSelect = document.getElementById("languageSelect");

    if (!languageSelect) {
        console.error("languageSelect not found");
        return;
    }


    // =========================================================
    // LOAD LANGUAGES FROM DATABASE
    // =========================================================

    async function loadLanguages() {

        try {

            const response = await fetch(
                "/api/languages?t=" + Date.now()
            );

            if (!response.ok) {
                throw new Error(
                    "Languages API error: " + response.status
                );
            }

            const data = await response.json();

            const languages = data.languages || [];

            languageSelect.innerHTML = "";

            languages.forEach(function (language) {

                const option = document.createElement("option");

                option.value = language.code;

                option.textContent =
                    language.native_name ||
                    language.name ||
                    language.code;

                languageSelect.appendChild(option);

            });

            if (languages.length === 0) {
                console.error("No active languages found in database.");
                return;
            }


            // =====================================================
            // RESTORE LAST SELECTED LANGUAGE
            // =====================================================

            const savedLanguage =
                localStorage.getItem("agrivision_language");

            const savedExists = languages.some(function (language) {
                return language.code === savedLanguage;
            });


            if (savedExists) {

                languageSelect.value = savedLanguage;

            } else {

                const english = languages.find(function (language) {
                    return language.code === "en";
                });

                if (english) {
                    languageSelect.value = "en";
                } else {
                    languageSelect.value = languages[0].code;
                }

            }


            console.log(
                "Database languages loaded:",
                languages.length
            );


            await changeLanguage(
                languageSelect.value
            );

        }

        catch (error) {

            console.error(
                "Language loading error:",
                error
            );

        }

    }


    // =========================================================
    // LOAD TRANSLATIONS FROM DATABASE
    // =========================================================

    async function changeLanguage(language) {

        if (!language) {
            return;
        }


        try {

            console.log(
                "Changing language to:",
                language
            );


            const response = await fetch(
                "/api/translations/" +
                encodeURIComponent(language) +
                "?t=" +
                Date.now()
            );


            if (!response.ok) {
                throw new Error(
                    "Translation API error: " +
                    response.status
                );
            }


            const data = await response.json();

            const translations =
                data.translations || {};


            console.log(
                "Translations received:",
                Object.keys(translations).length
            );


            // =====================================================
            // APPLY TRANSLATIONS AUTOMATICALLY
            // =====================================================

            document
                .querySelectorAll("[data-i18n]")
                .forEach(function (element) {

                    const key =
                        element.getAttribute("data-i18n");

                    if (
                        key &&
                        Object.prototype.hasOwnProperty.call(
                            translations,
                            key
                        )
                    ) {

                        element.textContent =
                            translations[key];

                    }

                });


            // =====================================================
            // SAVE LANGUAGE
            // =====================================================

            localStorage.setItem(
                "agrivision_language",
                language
            );


            console.log(
                "Language applied:",
                language
            );

        }

        catch (error) {

            console.error(
                "Translation error:",
                error
            );

        }

    }


    // =========================================================
    // DROPDOWN CHANGE
    // =========================================================

    languageSelect.addEventListener(
        "change",
        async function () {

            await changeLanguage(
                this.value
            );

        }
    );


    // =========================================================
    // START
    // =========================================================

    await loadLanguages();

});