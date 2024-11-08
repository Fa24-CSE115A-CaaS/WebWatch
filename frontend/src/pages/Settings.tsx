import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Settings = () => {
    const [activeTab, setActiveTab] = useState("vertical-tab-1");

    const navigate = useNavigate();

    const handleTabClick = (tabId: string) => {
        setActiveTab(tabId);
    };

    const uploadProfileImage = () => {
        // Click the image input
        // Listen for change event
        // Get the file
        // Convert file to url data
        // Set the image source to the url
        let input = document.getElementById("profileImageInput") as HTMLInputElement;
        input.onchange = function() {
            let file = input.files ? input.files[0] : null;
            if (file) {
                let reader = new FileReader();
                reader.readAsDataURL(file);
                reader.onload = function() {
                    let image = document.getElementById("profileImage") as HTMLImageElement;
                    image.src = reader.result as string;
                    // TODO: Send the image to the server
                }
            }
        };
        input.click();
    };

    const updateAccount = () => {
        let token = localStorage.getItem("access_token");
        if (!token) {
            navigate("/auth");
            return;
        }
        let email = (document.getElementById("form_email") as HTMLInputElement).value;
        let password = (document.getElementById("form_password") as HTMLInputElement).value;
        if (email && RegExp("^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$").test(email)) {
            alert("Please enter a valid email");
            return;
        }
        if (password) {
            if (password !== (document.getElementById("form_confirm_password") as HTMLInputElement).value) {
                alert("Passwords do not match");
                return;
            } else if (password.length < 8) {  
                alert("Password must be at least 8 characters long");
                return;
            }
        }
        let contents = {} as any;
        if (email) contents["email"] = email;
        if (password) contents["password"] = password;
        axios.put("/users/update", { headers: { Authorization: `Bearer ${token}` }, data: { contents } })
    }

    const deleteAccount = () => {
        let token = localStorage.getItem("access_token");
        if (!token) {
            navigate("/auth");
            return;
        }
        axios.delete("/users/delete", { headers: { Authorization: `Bearer ${localStorage.getItem("access_token")}` } })
    }

    return (
        <div className="mx-auto mt-8 min-h-screen w-1/2 rounded text-text">
            <div className="flex">
                {/* Column 1 */}
                <nav
                    className="min-h-screen w-max overflow-hidden rounded-l-xl border-2 border-solid
            border-border bg-secondary text-left"
                >
                    <div
                        className="rounded-tl-xl"
                        aria-label="Tabs"
                        role="tablist"
                        aria-orientation="vertical"
                    >
                        <button
                            type="button"
                            className={`w-full whitespace-nowrap p-4 text-left
                ${activeTab === "vertical-tab-1" ? "bg-primary" : ""}`}
                            id="vertical-tab-1"
                            aria-selected={activeTab === "vertical-tab-1"}
                            data-hs-tab="#vertical-tab-1"
                            aria-controls="vertical-tab-1"
                            role="tab"
                            onClick={() => handleTabClick("vertical-tab-1")}
                        >
                            Account
                        </button>
                        <button
                            type="button"
                            className={`w-full whitespace-nowrap p-4 text-left
                ${activeTab === "vertical-tab-2" ? "bg-primary" : ""}`}
                            id="vertical-tab-2"
                            aria-selected={activeTab === "vertical-tab-2"}
                            data-hs-tab="#vertical-tab-2"
                            aria-controls="vertical-tab-2"
                            role="tab"
                            onClick={() => handleTabClick("vertical-tab-2")}
                        >
                            Global Variables
                        </button>
                        <button
                            type="button"
                            className={`w-full whitespace-nowrap p-4 text-left
                ${activeTab === "vertical-tab-3" ? "bg-primary" : ""}`}
                            id="vertical-tab-3"
                            aria-selected={activeTab === "vertical-tab-3"}
                            data-hs-tab="#vertical-tab-3"
                            aria-controls="vertical-tab-3"
                            role="tab"
                            onClick={() => handleTabClick("vertical-tab-3")}
                        >
                            Account Linking
                        </button>
                    </div>
                </nav>

                {/* Column 2 */}
                <div className="w-full rounded-r-xl border-y-2 border-r-2 border-solid border-border bg-primary">
                    <div className="m-5 px-10 py-6">
                        {/* Main account settings content */}
                        {activeTab === "vertical-tab-1" && (
                            <>
                                <h1 className="mb-4 text-3xl">Account</h1>
                                <p className="mb-4">Change your account information</p>
                                <div className="mt-4 flex pb-4">
                                    <img id="profileImage" className="rounded-full size-32" onClick={() => uploadProfileImage()}></img>
                                    <div className="my-auto ml-4">
                                        <h2 className="mb-2 text-xl">Profile Picture</h2>
                                        <input type="file" id="profileImageInput" className="invisible" accept="image/png image/jpeg" />
                                        <button
                                            className="mr-4 mt-4 rounded-lg border-2 border-solid border-info p-1 px-8 text-base
                        text-info"
                                            onClick={() => uploadProfileImage()}
                                        >
                                            Upload
                                        </button>
                                        <button className="mt-2 rounded-lg border-2 border-solid border-error p-1 px-8 text-base text-error">
                                            Remove
                                        </button>
                                    </div>
                                </div>
                                <form className="pb-4">
                                    <label className="mb-2 block text-lg">Email</label>
                                    <input
                                        id="form_email"
                                        type="email"
                                        className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                                    />
                                    <h2 className="my-8 mb-4 text-2xl">Reset Password</h2>
                                    <label className="mb-2 block text-lg">Password</label>
                                    <input
                                        id="form_password"
                                        type="password"
                                        className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                                    />
                                    <label className="mb-2 block text-lg">Confirm Password</label>
                                    <input
                                        id="form_confirm_password"
                                        type="password"
                                        className="mb-4 w-full rounded-lg border border-border bg-secondary p-2 outline-none"
                                    />
                                    <button className="mt-4 rounded-lg bg-accent p-2 px-16 text-text-contrast hover:bg-accent-hover"
                                        onClick={() => updateAccount()}
                                    >
                                        Save
                                    </button>
                                </form>
                                <h2 className="my-8 mb-4 text-2xl">Danger Zone</h2>
                                <button className="rounded-lg bg-error px-3 py-2"
                                    onClick={() => deleteAccount()}
                                >
                                    Delete my account
                                </button>
                            </>
                        )}
                        {/* Global variable settings */}
                        {activeTab === "vertical-tab-2" && (
                            <>
                                <h1 className="mb-4 text-3xl">Global Variables</h1>
                                <p>Manage your global variables here.</p>
                            </>
                        )}
                        {/* Account linking settings */}
                        {activeTab === "vertical-tab-3" && (
                            <>
                                <h1 className="mb-4 text-3xl">Account Linking</h1>
                                <p>Link your account with other services.</p>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Settings;
