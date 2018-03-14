# -*- coding: utf-8 -*-

schedule = """\
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="description" content="">
        <meta name="author" content="">
        <title>Horaire des associés</title>
        <style type="text/css">
            body
{
    font-size: 12px;
}

.beglogo
{
    display: inline-block;
    float: left;
    height: 48px;
    margin: 15px;
}

.reporttitle
{
    display: inline-block;
    float: right;
    text-align: right;
}

.container
{
    clear: both;
}

.section-full
{
    width: 100%;
    margin-bottom: 10px;
}

.section-large
{
    width: 60%;
    float: left;
}

.section-small
{
    width: 20%;
    float: left;
}

.panel
{
    margin-left: 5px;
    margin-right: 5px;
    background-color: #fff;
    border: 1px solid #ddd;
    border-radius: 4px;
    -webkit-box-shadow: 0 1px 1px rgba(0,0,0,.05);
    box-shadow: 0 1px 1px rgba(0,0,0,.05);
}

.panel-heading
{
    color: #333;
    background-color: #f5f5f5;
    padding: 5px 10px;
    border-bottom: 1px solid #ddd;
    border-top-right-radius: 3px;
    border-top-left-radius: 3px;
}

.panel-title
{
    margin-top: 0;
    margin-bottom: 0;
    font-size: 16px;
    color: inherit;
}

.panel-body
{
    padding: 10px 0px;
}

.panel-body::before, .panel-body::after
{
    content: " ";
    display: table;
    clear: both;
}

.container::before, .container::after
{
    content: " ";
    display: table;
    clear: both;
}

.table
{
    width: 100%;
    max-width: 100%;
    background-color: transparent;
    border-spacing: 0;
    border-collapse: collapse;
}

.table>thead:first-child>tr:first-child>th
{
    border-top: 0;
}

.table>thead>tr>th
{
    vertical-align: bottom;
    border-bottom: 2px solid #ddd;
    text-align: left;
}

th
{
    text-align: left;
    width: 12%;
}

th:first-child
{
    width: 16%;
}

.table>tbody>tr:nth-of-type(odd)
{
    background-color: #f9f9f9;
}

.table>tbody>tr.highlight
{
    background-color: #ffffa9;
}

.table>tbody>tr>td, .table>tbody>tr>th, .table>tfoot>tr>td, .table>tfoot>tr>th, .table>thead>tr>td, .table>thead>tr>th
{
    padding: 5px;
    line-height: 1.0;
    vertical-align: middle;
    border-top: 1px solid #ddd;
}

.table>tbody>tr>td
{
    border-left: 1px solid #ddd;
}

.table>tbody>tr>td:first-child
{
    border-left: none;
}

.table>tbody>tr:last-child
{
    border-bottom: 1px solid #ddd;
}

.label-table>tbody>tr:nth-of-type(odd)
{
    background-color: #ffffff;
}

.label-table>tbody>tr>td
{
    width: 12.5%;
}

.red
{
    background-color: #ffcdd2;
}
.pink
{
    background-color: #f8bbd0;
}
.purple
{
    background-color: #e1bee7;
}
.deep-purple
{
    background-color: #d1c4e9;
}
.indigo
{
    background-color: #c5cae9;
}
.blue
{
    background-color: #bbdefb;
}
.light-blue
{
    background-color: #b3e5fc;
}
.cyan
{
    background-color: #b2ebf2;
}
.teal
{
    background-color: #b2dfdb;
}
.green
{
    background-color: #c8e6c9;
}
.light-green
{
    background-color: #dcedc8;
}
.lime
{
    background-color: #f0f4c3;
}
.yellow
{
    background-color: #fff9c4;
}
.amber
{
    background-color: #ffecb3;
}
.orange
{
    background-color: #ffe0b2;
}
.deep-orange
{
    background-color: #ffccbc;
}

</style>
    </head>
    <body>
        <img src="data:image/png;base64,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" class="beglogo"/>
        <div class="reporttitle">
            <h1>Horaire des associés</h1>
            <h3>Semaine du {{ datefrom }} au {{ dateto }}</h3>
        </div>
        <div class="container">
            <div class="section-full">
                <div class="panel">
                    <div class="panel-heading">
                        <h3 class="panel-title">Horaire des associés</h3>
                    </div>
                    <div class="panel-body">
                        <table class="table">
                            <thead>
                                <tr>
                                    <th>Nom de l'associé</th>
                                    <th>Dimanche</th>
                                    <th>Lundi</th>
                                    <th>Mardi</th>
                                    <th>Mercredi</th>
                                    <th>Jeudi</th>
                                    <th>Vendredi</th>
                                    <th>Samedi</th>
                                </tr>
                            </thead>
                            <tbody>
                                % for emp in sched:
                                <tr>
                                    <td>{{ emp['name'] }}</td>
                                    % for i, shift in enumerate(emp['shifts']):
                                    <td class="{{ labels.get(emp['labels'][i], '') }}">{{ shift }}</td>
                                    % end
                                </tr>
                                % end
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            <div class="section-full">
                <div class="panel">
                    <div class="panel-heading">
                        <h3 class="panel-title">Étiquettes des quarts</h3>
                    </div>
                    <div class="panel-body">
                        <table class="table label-table">
                            <tbody>
                                <tr>
                                    % for i, (labelname, labelclass) in enumerate(labels.iteritems()):
                                    % if i > 0 and i % 8 == 0:
                                    </tr><tr>
                                    % end
                                    <td class="{{ labelclass }}">{{ labelname }}</td>
                                    % end
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </body>
</html>
"""