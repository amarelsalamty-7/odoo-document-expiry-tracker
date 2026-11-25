/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class DocumentDashboard extends Component {
    static template = "document_expiry_tracker.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });

        onWillStart(async () => {
            await this.loadData();
        });
    }

    async loadData() {
        const data = await this.orm.call(
            "document.tracker",
            "get_dashboard_data",
            []
        );
        this.addPercentages(data.by_status);
        this.addPercentages(data.by_type);
        this.state.data = data;
    }

    // Bar width relative to the biggest value in the chart
    addPercentages(items) {
        const max = Math.max(1, ...items.map((item) => item.count));
        for (const item of items) {
            item.pct = Math.round((item.count / max) * 100);
        }
    }

    openItem(item) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: item.label,
            res_model: item.model,
            views: [
                [false, "list"],
                [false, "form"],
            ],
            domain: item.domain,
        });
    }

    async refresh() {
        await this.loadData();
    }
}

registry.category("actions").add("document_expiry_dashboard", DocumentDashboard);