var countrySateCityinfo = {
    Cardiologists: {
            "Dr. Cardio1": {
                Morning: ["8am - 9am", "9am-10am"],
                Afternoon :["Doctor not available"],
                Evening :["6pm-7pm","7pm-8pm"]
            },
            "Dr. Cardio2": {
                Morning: ["9am - 10am", "11am-12am"],
                Afternoon :["3pm - 4pm"],
                Evening :["7pm-8pm"]
            }

        },

    Dermatologists: {
        "Dr. Dermat1": {
            Morning: ["8am - 9am", "9am-10am"],
            Afternoon :["Doctor not available"],
            Evening :["7pm-8pm"]
        },
        "Dr. Dermat2": {
            Morning: ["9am - 10am", "11am-12am"],
            Afternoon :["3pm - 4pm"],
            Evening :["7pm-8pm"]
        }

    },

    FamilyPhysicians: {
        "Dr. Physc1": {
            Morning: ["8am - 9am", "9am-10am"],
            Afternoon :["Doctor not available"],
            Evening :["6pm-7pm","7pm-8pm"]
        },
        "Dr. Physc2": {
            Morning: ["9am - 10am", "11am-12am"],
            Afternoon :["3pm - 4pm"],
            Evening :["7pm-8pm"]
        }
    },

    Gynecologists: {
        "Dr. Gynec1": {
            Morning: ["8am - 9am", "9am-10am"],
            Afternoon :["Doctor not available"],
            Evening :["7pm-8pm"]
        },
        "Dr. Gynec2": {
            Morning: ["9am - 10am", "11am-12am"],
            Afternoon :["3pm - 4pm"],
            Evening :["6pm-7pm","7pm-8pm"]
        }
    },

    Neurologists: {
        "Dr. Neuro1": {
            Morning: ["8am - 9am", "9am-10am"],
            Afternoon :["Doctor not available"],
            Evening :["7pm-8pm"]
        },
        "Dr. Neuro2": {
            Morning: ["9am - 10am", "11am-12am"],
            Afternoon :["3pm - 4pm"],
            Evening :["6pm-7pm","7pm-8pm"]
        }
    },

    Psychiatrists: {
        "Dr. Psych1": {
            Morning: ["8am - 9am", "9am-10am"],
            Afternoon :["Doctor not available"],
            Evening :["6pm-7pm","7pm-8pm"]
        },
        "Dr. Psych2": {
            Morning: ["9am - 10am", "11am-12am"],
            Afternoon :["3pm - 4pm"],
            Evening :["6pm-7pm"]
        }
    },


    
}

window.onload = function(){
    const selectCountry = document.getElementById('country'),
        selectState = document.getElementById('state'),
        selectCity = document.getElementById('city'),
        selectZip = document.getElementById('zip'),
        selects = document.querySelectorAll('select')

        selectState.disabled = true
        selectCity.disabled = true
        selectZip.disabled = true

        selects.forEach(select => {
            if(select.disabled == true){
                select.style.cursor = "auto"
            }
            else{
                select.style.cursor = "pointer"
            }
        })

        for(let country in countrySateCityinfo){
            // console.log(country);
            selectCountry.options[selectCountry.options.length] = new Option(country, country)
        }


        // country change
        selectCountry.onchange = (e) =>{
            
            selectState.disabled = false
            selectCity.disabled = true
            selectZip.disabled = true

            selects.forEach(select => {
                if(select.disabled == true){
                    select.style.cursor = "auto"
                }
                else{
                    select.style.cursor = "pointer"
                }
            })

            selectState.length = 1
            selectCity.length = 1
            selectZip.length = 1

            for(let state in countrySateCityinfo[e.target.value]){
                // console.log(state);
                selectState.options[selectState.options.length] = new Option(state, state)
            }
        }

        // state change
        selectState.onchange = (e) =>{
            selectCity.disabled = false
            selectZip.disabled = true

            selects.forEach(select => {
                if(select.disabled == true){
                    select.style.cursor = "auto"
                }
                else{
                    select.style.cursor = "pointer"
                }
            })

            selectCity.length = 1
            selectZip.length = 1

            for(let city in countrySateCityinfo[selectCountry.value][e.target.value]){
                // console.log(city);
                selectCity.options[selectCity.options.length] = new Option(city, city)
            }
        }

        // change city
        selectCity.onchange = (e) =>{
            selectZip.disabled = false

            selects.forEach(select => {
                if(select.disabled == true){
                    select.style.cursor = "auto"
                }
                else{
                    select.style.cursor = "pointer"
                }
            })
            
            selectZip.length = 1

            let zips = countrySateCityinfo[selectCountry.value][selectState.value][e.target.value]
            
            for(let i=0; i<zips.length; i++){
                selectZip.options[selectZip.options.length] = new Option(zips[i], zips[i])
            }
        }
}
