function combineData() {
    var masterSheet = "Master";

    var master_spreadsheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(masterSheet);
    var columnNumber = master_spreadsheet.getLastColumn();
    var rowNumber = master_spreadsheet.getLastRow() > 1 ? master_spreadsheet.getLastRow() : 2;

    master_spreadsheet.getRange(2, 1, rowNumber - 1, columnNumber).clearContent();

    var labels = master_spreadsheet.getRange(1, 1, 1, columnNumber).getValues()[0];


    labels.forEach(function(label, i) {
            if (label == 'sheet') {
                sheetNameArray = fillArray(label master_spreadsheet.getRange(2, i + 1, colValues.length, 1).setValues(values)
                }
                else {
                    var colValues = getCombinedColumnValues(label, masterSheet);
                    master_spreadsheet.getRange(2, i + 1, colValues.length, 1).setValues(colValues);
                }

            })
    }

    function fillArray(value, len) {
        var arr = [];
        for (var i = 0; i < len; i++) {
            arr.push(value);
        }
        return arr;
    }

    function getCombinedColumnValues(label, masterSheetName) {

        var sheets = SpreadsheetApp.getActiveSpreadsheet().getSheets();

        var colValues = [];

        for ([sheetNumber, sheet] in sheets) {
            var sheetName = sheet.getSheetName();
            if (sheetName !== masterSheetName) {
                var tempValues = getColumnValues(label, sheetName);
                colValues = colValues.concat(tempValues);
            }
        }

        return colValues;
    }


    function getColumnValues(label, sheetName) {
        var master_spreadsheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
        var colIndex = getColumnIndex(label, sheetName);
        var numRows = master_spreadsheet.getLastRow() - 1;
        var colValues = master_spreadsheet.getRange(2, colIndex, numRows, 1).getValues();
        return colValues;
    }


    function getColumnIndex(label, sheetName) {
        var master_spreadsheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(sheetName);
        var columnNumber = master_spreadsheet.getLastColumn();
        var lookupRangeValues = master_spreadsheet.getRange(1, 1, 1, columnNumber).getValues()[0];
        var index = lookupRangeValues.indexOf(label) + 1;
        return index;
    }