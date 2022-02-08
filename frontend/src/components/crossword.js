import React, { useState, useEffect } from 'react';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';

const Crossword = ({ grid }) => {

    const renderRow = (row) => {
        return (row.map(cell => {return (<td key={cell.cords}>{cell.contents}</td>)}))
    }

    return <table>
            <tbody>
                {grid.length > 0 ? grid.map((row, i) =>
                { return (<tr key={i}>{renderRow(row)}</tr>)}
                ) : console.log("VIGA")}
            </tbody>
            </table>

}

export default Crossword