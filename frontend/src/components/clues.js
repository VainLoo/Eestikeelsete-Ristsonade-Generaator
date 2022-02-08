import React, { useState, useEffect } from 'react';
import { Fieldset } from 'primereact/fieldset';
import { DataTable } from 'primereact/datatable';
import { Column } from 'primereact/column';
import { Card } from 'primereact/card';

const Clues = ({ words }) => {
    return <div>
        <Card title="Küsimused">
        <Fieldset legend="Vasakule" toggleable>
            <div className="card">
                    <DataTable value={words.across} size="small" responsiveLayout="scroll">
                        <Column field="index" header="Number"></Column>
                        <Column field="clue" header="Vihje"></Column>
                    </DataTable>
            </div>
        </Fieldset>
        <Fieldset legend="Alla" toggleable>
        <div className="card">
                    <DataTable value={words.down} size="small" responsiveLayout="scroll">
                        <Column field="index" header="Number"></Column>
                        <Column field="clue" header="Vihje"></Column>
                    </DataTable>
            </div>
        </Fieldset>
        </Card>
    </div>
}

export default Clues