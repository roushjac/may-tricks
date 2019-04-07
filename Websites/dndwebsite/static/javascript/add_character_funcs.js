var num_of_items = 1;
var num_of_spells = 1;
var num_of_features = 1;

/* Create event listener on 'add equipment' button */
const equip_table = document.getElementById('equip_table');
const equip_button = document.getElementById('add_equip_button');
equip_button.addEventListener('click', () => { /* Using ES6 anon function */
    num_of_items += 1;
    const new_equip = document.createElement('tr');
    /* Make item name cell */
    const item_name_cell = document.createElement('td');
    const item_name_input = document.createElement('input');
    item_name_input.setAttribute('type', 'text');
    item_name_input.setAttribute('name', 'item_'+String(num_of_items));
    item_name_cell.appendChild(item_name_input);
    /* Make item description cell */
    const item_desc_cell = document.createElement('td');
    const item_desc_input = document.createElement('textarea');
    item_desc_input.setAttribute('name', 'item_'+String(num_of_items)+'_desc');
    item_desc_cell.appendChild(item_desc_input);
    /* Make delete button */
    const del_button_cell = document.createElement('td');
    const del_button = document.createElement('button');
    del_button.setAttribute('type', 'button');
    del_button.setAttribute('onclick', 'deleteRow(event)');
    del_button.appendChild(document.createTextNode('Delete'));
    del_button_cell.appendChild(del_button);
    /* Append cells to table row */
    new_equip.appendChild(item_name_cell);
    new_equip.appendChild(item_desc_cell);
    new_equip.appendChild(del_button_cell);
    /* Append row to original table */
    equip_table.appendChild(new_equip);
});

/* Create event listener on 'add spells' button */
const spells_table = document.getElementById('spells_table');
const spell_button = document.getElementById('add_spell_button');
spell_button.addEventListener('click', () => { /* Using ES6 anon function */
    num_of_spells += 1;
    const new_spell = document.createElement('tr');
    /* Make spell name cell */
    const spell_name_cell = document.createElement('td');
    const spell_name_input = document.createElement('input');
    spell_name_input.setAttribute('type', 'text');
    spell_name_input.setAttribute('name', 'item_'+String(num_of_spells));
    spell_name_cell.appendChild(spell_name_input);
    /* Make delete button */
    const del_button_cell = document.createElement('td');
    const del_button = document.createElement('button');
    del_button.setAttribute('type', 'button');
    del_button.setAttribute('onclick', 'deleteRow(event)');
    del_button.appendChild(document.createTextNode('Delete'));
    del_button_cell.appendChild(del_button);
    /* Append cells to table row */
    new_spell.appendChild(spell_name_cell);
    new_spell.appendChild(del_button_cell);
    /* Append row to original table */
    spells_table.appendChild(new_spell);
})

/* Create event listener on 'add feature' button */
const features_table = document.getElementById('features_table');
const feature_button = document.getElementById('add_feature_button');
feature_button.addEventListener('click', () => { /* Using ES6 anon function */
    num_of_features += 1;
    const new_feature = document.createElement('tr');
    /* Make feature name cell */
    const feature_name_cell = document.createElement('td');
    const feature_name_input = document.createElement('input');
    feature_name_input.setAttribute('type', 'text');
    feature_name_input.setAttribute('name', 'item_'+String(num_of_features));
    feature_name_cell.appendChild(feature_name_input);
    /* Make feature description cell */
    const feature_desc_cell = document.createElement('td');
    const feature_desc_input = document.createElement('textarea');
    feature_desc_input.setAttribute('name', 'item_'+String(num_of_items)+'_desc');
    feature_desc_cell.appendChild(feature_desc_input);
    /* Make delete button */
    const del_button_cell = document.createElement('td');
    const del_button = document.createElement('button');
    del_button.setAttribute('type', 'button');
    del_button.setAttribute('onclick', 'deleteRow(event)');
    del_button.appendChild(document.createTextNode('Delete'));
    del_button_cell.appendChild(del_button);
    /* Append cells to table row */
    new_feature.appendChild(feature_name_cell);
    new_feature.appendChild(feature_desc_cell);
    new_feature.appendChild(del_button_cell);
    /* Append row to original table */
    features_table.appendChild(new_feature);
});

/* Using a much more elegant function for the delete button */
function deleteRow(e) {
    const this_row = e.target.parentElement.parentElement; /* Parent of button is cell, parent of cell is row */
    this_row.remove();
}