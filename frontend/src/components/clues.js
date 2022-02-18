import React from 'react';
import { Fieldset } from 'primereact/fieldset';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Card } from 'primereact/card';
import { Accordion, AccordionTab } from 'primereact/accordion';

const Clues = ({ words, check }) => {
    return <div>
        <Card title="Küsimused">
        <Accordion multiple activeIndex={[]}>
        <AccordionTab header="Paremale">
            <div className="card">
                    <DataTable value={words.across} size="small" responsiveLayout="scroll" emptyMessage="Puudub ristsõna">
                        <Column field="index" header="Number"></Column>
                        <Column field="clue" header="Vihje" ></Column>
                        {check && <Column field="word" header="Vastus"></Column>}
                    </DataTable>
            </div>
            </AccordionTab>
            <AccordionTab header="Alla">
        <div className="card">
                    <DataTable value={words.down} size="small" responsiveLayout="scroll" emptyMessage="Puudub ristsõna">
                        <Column field="index" header="Number"></Column>
                        <Column field="clue" header="Vihje"></Column>
                        {check && <Column field="word" header="Vastus"></Column>}
                    </DataTable>
            </div>
            </AccordionTab>
        </Accordion>
        </Card>
    </div>
}

export default Clues