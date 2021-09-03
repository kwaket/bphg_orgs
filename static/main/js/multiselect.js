(function () {

    const generateItemCloseBtn = () => {
        const btn = document.createElement('small')
        btn.classList.add('bi')
        btn.classList.add('bi-x-lg')
        btn.classList.add('remove-item')
        return btn
    }

    const generateSelectedItem = (select, itemName, selectedItemsContainer, datalist) => {
        const selectedElement = document.createElement('div')
        selectedElement.classList.add('selected-item')
        selectedElement.classList.add('bg-info')
        selectedElement.appendChild(document.createTextNode(itemName))
        selectedElement.appendChild(document.createTextNode(' '))
        let closeBtn = generateItemCloseBtn()
        selectedElement.appendChild(closeBtn)

        selectedElement.getElementsByClassName('remove-item')[0].addEventListener('click', removeItem);

        function removeItem(e) {
            deselectItem(select, e.target.parentNode.textContent.trim(), selectedItemsContainer, datalist)
        }


        return selectedElement
    }

    const extractSelectElem = (wrapper) => {
        const selectElem = wrapper.getElementsByTagName('select')[0],
            label = wrapper.getElementsByTagName('label')[0],
            options = Array.from(selectElem.children).map(x => x.textContent)
        return {
            id: selectElem.id,
            name: selectElem.getAttribute('name'),
            label: label,
            options: options,
            select: selectElem
        }
    }

    const fillDatalist = (datalistElem, optionsList) => {
        optionsList.forEach(option => {
            const optionElem = document.createElement('option');
            optionElem.appendChild(document.createTextNode(option));
            datalistElem.appendChild(optionElem)
        });
    }

    const generateDatalist = (id, options) => {
        const datalist = document.createElement('datalist');
        datalist.id = id + '-list';

        fillDatalist(datalist, options)

        return datalist
    }


    const updasteDatalist = (datalist, select) => {
        datalist.innerHTML = '';
        let options = Array.from(select.children).filter(x => !x.selected)
        options = options.map(x => x.textContent)
        fillDatalist(datalist, options)
    }

    const selectOption = (selectedItemText, options, selected) => {
        for (let option of options) {
            if (option.textContent === selectedItemText) {
                option.selected = selected
                break
            }
        }
    }

    const selecteItem = (selectElem, itemText, selectedItemsContainer, datalist) => {
        // select item in original select
        selectOption(itemText, selectElem.children, true)
        // draw selected items in input box
        let selectedElement = generateSelectedItem(selectElem, itemText, selectedItemsContainer, datalist)
        selectedItemsContainer.append(selectedElement)
        // update datalist from select options
        updasteDatalist(datalist, selectElem);
    }

    const deselectItem = (selectElem, itemText, selectedItemsContainer, datalist) => {
        // remove item in original select
        selectOption(itemText, selectElem.children, false)
        // remove item in input box
        for (let selectedItem of selectedItemsContainer.children) {
            if (selectedItem.textContent.trim() === itemText) {
                selectedItem.parentNode.removeChild(selectedItem)
                break
            }
        }
        // update datalist from select options
        updasteDatalist(datalist, selectElem)
    }

    const generateCustomMultiselectField = (id, name, oldLabel, options, select) => {
        oldLabel.style.display = "none";
        const wrapper = document.createElement('div'),
            labelText = oldLabel.textContent,
            label = document.createElement('label'),
            labelContent = document.createTextNode(labelText),
            wrapperField = document.createElement('div'),
            selectedItemsContainer = document.createElement('div'),
            inputField = document.createElement('input');

        label.appendChild(labelContent);
        wrapperField.classList.add('custom-multiselect-phantom');
        wrapperField.classList.add('form-control');
        selectedItemsContainer.classList.add('selected-items')
        wrapperField.append(selectedItemsContainer)
        wrapperField.appendChild(inputField);
        let datalist = generateDatalist(id, options)
        wrapperField.appendChild(datalist)

        inputField.addEventListener('input', onInput);
        inputField.addEventListener('keyup', onKeyup);
        inputField.addEventListener('focus', focusWrapperOn);
        inputField.addEventListener('focusout', focusWrapperOff);

        function onInput(e) {
            let input = e.target,
                val = input.value,
                list = input.getAttribute('list'),
                options = document.getElementById(list).childNodes;


            for (let option of options) {
                let itemText = option.innerText
                if (itemText === val) {
                    selecteItem(select, itemText, selectedItemsContainer, datalist);
                    inputField.value = ''
                    break;
                }
            }
        }

        function onKeyup(e) {
            let input = e.target,
                val = input.value,
                list = input.getAttribute('list'),
                options = document.getElementById(list).childNodes,
                selectedItems = document.getElementsByClassName('selected-items')[0];

            if (e.code === 'Backspace' && val === '') {
                let lastItem = selectedItems.children[selectedItems.children.length - 1];
                let lastItemText = lastItem.textContent.trim();
                deselectItem(select, lastItemText, selectedItemsContainer, datalist)
            }
        }

        function focusWrapperOn(e) {
            wrapperField.classList.add('focused')
        }

        function focusWrapperOff(e) {
            wrapperField.classList.remove('focused')
        }
        wrapper.appendChild(label);
        wrapper.appendChild(wrapperField)
        inputField.id = id
        inputField.setAttribute('list', id + '-list')

        return wrapper;
    }

    const createCustomMultiselect = (selectWrapperElem) => {
        let {
            name,
            id,
            label,
            options,
            select
        } = extractSelectElem(selectWrapperElem)

        const customMultiSelect = generateCustomMultiselectField(id, name, label, options, select)
        select.style.display = "none";
        return customMultiSelect
    }


    const replaceSelect = (select_wrapper) => {
        let customMultiSelect = createCustomMultiselect(select_wrapper);
        select_wrapper.parentNode.insertBefore(customMultiSelect, select_wrapper);
    }

    const replaceSelects = (selectsElements) => {
        for (let sel of selectsElements) {
            replaceSelect(sel)
        }
    }

    globalThis.replaceSelect = replaceSelect;
    globalThis.replaceSelects = replaceSelects;
})()
