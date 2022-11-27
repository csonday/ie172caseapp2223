# Table of Contents
- [Table of Contents](#table-of-contents)
- [Setting up a One-to-Many Form](#setting-up-a-one-to-many-form)
- [Setup the DB](#setup-the-db)
  - [Purchase Order](#purchase-order)
  - [Items](#items)
  - [Purchase Order Items](#purchase-order-items)
- [Parts of the Interface](#parts-of-the-interface)
  - [Modal for Line Items (`poprof_modal`)](#modal-for-line-items-poprof_modal)
  - [`dcc.Store` Elements](#dccstore-elements)
  - [Callbacks](#callbacks)
- [Operations Involved](#operations-involved)
  - [Adding a New Line Item](#adding-a-new-line-item)
  - [Setting up Table of Line Items](#setting-up-table-of-line-items)
  - [Editing A Line Item](#editing-a-line-item)
  - [Loading a Purchase Order in Edit Mode](#loading-a-purchase-order-in-edit-mode)
  - [Finishing up in Add/Edit Mode](#finishing-up-in-addedit-mode)
  - [Cancelling the Transaction in Add Mode](#cancelling-the-transaction-in-add-mode)
  - [Marking the PO as Deleted using Edit Mode](#marking-the-po-as-deleted-using-edit-mode)
- [Other Implementation Considerations or Variations](#other-implementation-considerations-or-variations)

# Setting up a One-to-Many Form

For this resource, a **Purchase Order scenario** will be considered where one purchase order can have multiple items with specific quantities. Take note that there may be many executions/variations of this particular implementation. Some of which may be mentioned later. 

Since the code is already available to you, this resource contains information on how to understand what is happening (rather than how to build the code). *To build this for your particular use*, you may simply copy the callbacks and replace the analogous elements (i.e. Outputs, inputs, states).
  

# Setup the DB
Run the following scripts to build the required db elements for this walkthrough.
## Purchase Order
```
CREATE TABLE po_transactions(
    po_id serial primary key not null,
    po_date date DEFAULT CURRENT_DATE not null,
    po_remarks varchar(256),
    po_delete_ind bool default false
);
```
## Items
```
CREATE TABLE items(
    item_id serial primary key not null,
    item_name varchar(32) unique not null
);

-- We need data rows for items since we need it to
-- build a transaction

INSERT INTO items (item_name)
VALUES
    ('monitor'),
    ('keyboard'),
    ('mouse'),
    ('mic'),
    ('camera');
```
## Purchase Order Items
```
CREATE TABLE po_items(
    po_item_id serial primary key not null,
    po_id int not null references po_transactions(po_id),
    item_id int not null references items(item_id),
    po_item_qty int not null,
    po_item_delete_ind bool default false,

    -- Need to ensure that the composite keys are unique
    CONSTRAINT po_items_unique UNIQUE(po_id, item_id)
);
```

___
# Parts of the Interface
## Modal for Line Items (`poprof_modal`)
For this implementation, a modal serves as a **pop-up form** for each line item. It will be used to add new line items, and edit/delete each line. 

PLS ADD A PHOTO


## `dcc.Store` Elements
These storage elements will be significant to store objects into the memory so that information is available when an add/edit/delete process is performed.

PLS ADD A LIST OF THE ELEMENTS

## Callbacks
At least five (5) callbacks will be required for this form:
1. `pageLoadOperations`
   -    This callback will be used for two purposes: (a) populating dropdowns and hiding add/edit-specific elements and (b) triggering another callback for populating PO fields

2. `queryPOdata`
    -    When the user wants to edit PO details (i.e. in edit mode), this callback pre-populates the PO information already present in the db
3. `toggleModal`
   -    This is the largest callback that controls the following: (a) opening and closing `po_modal`, (b) determining whether you are adding or editing a line item, (c) saving the line items to the db, and (d) updating the interface that displays the line items.
4. `clearFields`
   -    This callback populates the modal for line items, if necessary. 
        -    If you are **adding a line item**, it resets the fields in the modal to be blank. 
        -    If you are **editing a line item**, it pre-populates the fields with the saved details.
1. `finishTransaction`
   -    This callback does the following (a) checks if the PO has line items, and (b) cancels/deletes PO transactions.


# Operations Involved
For this section, follow the given pseudocode to understand how the code executes the tasks specified
## Adding a New Line Item
1. Clicking the "+ Add Line Item" (`poprof_addlinebtn`) button triggers `toggleModal` to open `poprof_modal`.
   -  Note that having incomplete PO details will prevent the modal from opening. This is because we will also create the PO record in the DB upon creating the first PO line item.
2. `clearFields` is also triggered via `poprof_addlinebtn`
3. When the modal shows, user inputs the data. 
4. Two possible actions: Cancel or Save
   1. Cancel via `poprof_cancellinebtn` Button
      1. `toggleModal` is triggered via the `n_clicks` property of `poprof_cancellinebtn` 
      2. If `poprof_cancelllinebtn` is identified as `eventid`, the modal simply closes
   2. Save via `poprof_savelinebtn`
      1. `toggleModal` is triggered via the `n_clicks` property of `poprof_savelinebtn` 
      2. If `poprof_savelinebtn` is identified as `eventid`, the following actions are executed
         1. Verify if inputs are correct. The `dbc.Alert()` item  with id = `poprof_linealert` is shown and its message is updated based on the input errors.
         2. Create a dictionary object `newlineitem` with the fields in the model
         3. After verifying that the modal is in add mode (`lineitemid` == 0), add `newlineitem` to the db. 
            -    The function `addPOLineItem()` does this task
            -    Note that if we do not have any line items yet, we save the PO transaction first so that we have a `po_id` to use. We run `createPOrecord()` to perfcorm this action.
            -    The PO id is saved to the callback variable `po_id` and the `dcc.Store()` element `poprof_poid`
         4. Query the line items given the PO using `queryPOLineItems(po_id)` as a dataframe. This will be used to create the table of line items in the interface.
            -    Note that some formating was done between creating the dataframe and `dbc.Table` object. [See next section](#setting-up-table-of-line-items).

## Setting up Table of Line Items
1. Make it a practice to align numbers to the right. For currencies, apply the function below to add a comma separator and to round the numbers to the nearest hundredths. 
   -    `df[col] = df[col].apply(lambda num: html.Div(f"{num:,.2f}", className='text-right'))` 

2. You can add an Item # column to label the line items.
   -    `df.insert(loc=0, column='Item #', value=[i+1 for i in len(df.index)])`
3. A button is added that can help us edit the line items. Note that the `id` for these buttons are dictionaries with keys `type` (the name for the family of buttons) and `index` (an indicator of the `po_item_id` to edit).
## Editing A Line Item
1. Clicking the "Modify" button (`id={'index':<po_item_id>, 'type': poprof_editlinebtn}`) will trigger `toggleModal` to open `poprof_modal`.
2.  `toggleModal` is triggered via the `n_clicks` property of `{'index':ALL, 'type': poprof_editlinebtn}`
    1.  We extract the `po_item_id` that triggered the callback.
    2.  We update the variable `lineitemid` to be equal to the `po_item_id`. 
    3.  The value of `lineitemid` is used by `toggleModal` to update the `dcc.Store` element `poprof_lineitemid`.
    4.  `poprof_modal` opens
3.  The fields are pre-populated according to `lineitemid` 
    1.  Change in `poprof_lineitemid` triggers the callback `clearFields`
    2.  Upon checking that `eventid == "poprof_lineitemid"` and `lineitemid != 0`, we query the data from the db related to `lineitemid`. See `getPOLineData(lineitemid)`.
    3.  The returned data is used to updated the values of the fields in `poprof_modal`.
4.  Saving changes via `poprof_savelinebtn`
    1.  Verify if inputs are correct. The `dbc.Alert()` item  with id = `poprof_linealert` is shown and its message is updated based on the input errors.
    2. Create a dictionary object `newlineitem` with the fields in the model
    3.  After verifying that the modal is in edit mode (`lineitemid` != 0), update the line item in the db using `updatePOLineItem(lineitemid)`.
    4.  Query the line items given the PO using `queryPOLineItems(po_id)` as a dataframe. This will be used to create the table of line items in the interface.

## Loading a Purchase Order in Edit Mode
The scenarios above assume that you are in `add mode` for the PO profile. The following shows how to load PO data in `edit mode`.

1. Upon checking the URL, the callback `pageLoadOperations` determines the mode for the page -- whether add or edit.
2. In add mode...
   1. Fill out the options for any dropdown. 
   2. Ensure that all the fields are blank.
3. In edit mode...
   1. Get `po_id` from url.
   2. Query data from the table `po_transactions` using `getBasicPODetails(po_id)`
      1. Use this data to update the general PO information using the same callback -- `pageLoadOperations`
   3. Update a 'dcc.Store' element `poprof_loadlineitems = 1` in `pageLoadOperations`
   4. Updating `poprof_loadlineitems` triggers the callback `toggleModal`. 
      - Activate the function `queryPOLineItems(po_id)` so that we can generate the table of line items.
      - Using `toggleModal`, update the `poprof_poid` so it contains the po_id. We can use this value to decide if we have to run `createPOrecord()` or not.


## Finishing up in Add/Edit Mode
1. `finishTransaction` is triggered via the `n_clicks` property of `poprof_savebtn` .
2. If `mode='add'` or `mode='edit' and not marked_as_delete`, run `checkPOLineItems(po_id)` to check if we have any line items. 
3. Display an error prompt if there are no line items detected.
## Cancelling the Transaction in Add Mode
**In case the user wishes not to pursue with the transaction**, they can click on the cancel button at the bottom of the form. This should set the `po_delete_ind = True` for the given po_id.

1. If the user is satisfied with the entries, there is a "Save PO" button that does not really do anything -- it's just a hyperlink that leads to `/po/po_home`.
2. If the user is not satisfied, the callback `finishTransaction` is triggered
   1. `finishTransaction` is triggered via the `n_clicks` property of `poprof_cancelbtn`
   2. Only proceed with cancelling in this manner if we are in Add Mode
      1. With `poprof_poid` as State, we can *delete* the PO using the function `deletePO(po_id)`

## Marking the PO as Deleted using Edit Mode
In this case, the user enters the edit mode and marks the transaction as deleted. 
1. If the user is not satisfied, the callback `finishTransaction` is triggered
   1. `finishTransaction` is triggered via the `n_clicks` property of `poprof_savebtn`
   2. Only proceed with cancelling in this manner if we are in Edit Mode and the checkbox `poprof_removePO` is ticked
      1. With `poprof_poid` as State, we can *delete* the PO using the function `deletePO(po_id)`


# Other Implementation Considerations or Variations
1. Since you are saving the PO in the DB *while the user is still completing the PO Data*, you may add checks to ensure that the required PO data is filled out (i.e. is there a transaction date chosen?)
2. Some forms **save all the PO details and line items at once** when the SAVE PO button is clicked. 
   1. Some do this if they only assign a po_id once the transaction is final and complete. This has the mindset that users who start the transaction must always complete the data before sending the data to the db.
   2. PRO: This interfaces with the db less often because the line items are stored in computer memory (i.e. dcc.Store). Less lags due to SELECT queries. 
   3. CON: Lags may happen due to use of computer memory. 

3. Some user different types of interface to enter data. This is entirely up to the developers and needs of the system.
