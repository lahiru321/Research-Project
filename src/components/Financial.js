import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'font-awesome/css/font-awesome.min.css';

const Financial = () => {
    const [isSidebarCollapsed, setSidebarCollapsed] = useState(false);

    const toggleSidebar = () => {
        setSidebarCollapsed(!isSidebarCollapsed);
    };

    return (
        <>
            <style>
                {`
                    .content {
                        width: 100%;
                        overflow-y: scroll;
                        height: 100vh;
                        transition: margin-left 0.3s; /* Smooth transition for content */
                    }

                    #sidebar {
                        position: sticky;
                        top: 0;
                        height: 100%;
                        z-index: 2;
                        transition: width 0.3s; /* Smooth transition for sidebar */
                    }

                    #sidebar.collapsed {
                        width: 27px; /* Width when collapsed */
                        overflow: hidden; /* Hide overflow when collapsed */
                    }

                    #sidebar .custom-menu {
                        position: absolute;
                    }

                    .logo {
                        font-size: 25px;
                    }

                    .black-text {
                        color: black;
                        font-weight: bold;
                    }

                    .wrapper.sidebar-collapsed .content {
                        margin-left: 60px; /* Adjust margin when sidebar is collapsed */
                    }
                `}
            </style>
            <div className={`wrapper d-flex align-items-stretch ${isSidebarCollapsed ? 'sidebar-collapsed' : ''}`}>
                <nav id="sidebar" className={isSidebarCollapsed ? 'collapsed' : ''}>
                    <div className="custom-menu">
                        <button type="button" id="sidebarCollapse" className="btn btn-primary" onClick={toggleSidebar}>
                            <i className="fa fa-bars"></i>
                            <span className="sr-only">Toggle Menu</span>
                        </button>
                    </div>
                    <div className="p-4 pt-5">
                        <ul className="list-unstyled components mb-5">
                            <h6 className="sidebar-heading mt-4 mb-1 black-text">Dashboard</h6>
                            <li className="nav-item">
                                <a className="nav-link p-2" href="/expenses">Expenses</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/income">Income</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/forecast">Forecast Expenses</a>
                            </li>
                            <h6 className="sidebar-heading mt-4 mb-1 black-text">SUMMARY</h6>
                            <li className="nav-item">
                                <a className="nav-link p-2" href="/stats">Expense Summary</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/income-summary">Income Summary</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/report">Reports</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/list_goals">Goals</a>
                            </li>
                            <h6 className="sidebar-heading mt-4 mb-1 black-text">Settings</h6>
                            <li className="nav-item">
                                <a className="nav-link p-2" href="/preferences">General</a>
                            </li>
                            <li className="nav-item p-2">
                                <a className="nav-link" href="/account">Account</a>
                            </li>
                        </ul>
                    </div>
                </nav>
                <div className="content">
                    {/* Add your content here */}
            <h2>Welcome to ExpenseWise</h2>
            <p>content goes here</p>
                </div>
            </div>
        </>
    );
};

export default Financial;
