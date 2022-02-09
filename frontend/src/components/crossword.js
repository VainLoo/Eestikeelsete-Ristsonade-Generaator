import React from 'react';
//import { DataTable } from 'primereact/datatable';
//import { Column } from 'primereact/column';
import Cell from './cell';
import '../styles/Crossword.css'

const Crossword = ({ grid }) => {

    const renderRow = (row) => {
        return (row.map(cell => { return (<td key={cell.cords}>{<Cell content={cell.contents}></Cell>}</td>) }))
    }

    return <table className='crossword'>
        <tbody>
            {grid.length > 0 ? grid.map((row, i) => { return (<tr key={i}>{renderRow(row)}</tr>) }
            ) : console.log("VIGA")}
        </tbody>
    </table>

}

export default Crossword