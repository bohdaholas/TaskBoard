import TaskList from "./TaskList";
import TaskListControl from "./TaskListControl";
import {useEffect, useState} from "react";
import TaskItemPopup from "./TaskItemPopup";

const TaskBoard = () => {
    const [controlState, setControlState] = useState({});
    const [showPopup, setShowPopup] = useState(false);
    const [popupTask, setPopupTask] = useState({});
    const [getInputData, setGetInputData] = useState(false);
    const facade_endpoint = 'http://localhost:2000'

    const handleChangeState = (current_control_state) => {
        console.log(current_control_state);
        setControlState(current_control_state);
    };

    const handlePopup = (task) => {
        console.log('handling popup');
        setShowPopup(true);
        setPopupTask(task);
    };

    const closePopup = () => {
        setShowPopup(false);
        setControlState({
            create_task_flag: false,
            edit_task_flag: false,
            remove_task_flag: false
        });
    };

    const handleCancel = () => {
        console.log('handling cancel');
        closePopup();
    };

    const handleSave = () => {
        console.log('handling save');
        setGetInputData(true);
    };

    const sendRequest = async (request_type, task) => {
        try {
            const members_ids = task.members_ids.split(',').map(memberId => parseInt(memberId.trim(), 10));
            const response = await fetch(facade_endpoint, {
                method: request_type,
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    _id: task._id,
                    title: task.title,
                    description: task.description,
                    members_ids: members_ids,
                    due_date: task.due_date,
                }),
            });
            if (response.ok) {
                console.log(request_type + ' request successful');
            } else {
                console.error(request_type + ' request failed');
            }
        } catch (error) {
            console.error('Error occurred during ' + request_type + 'request');
            console.error(error);
        }
    }

    const handleSendData = async (taskData) => {
        console.log('sending data', taskData);
        setGetInputData(false);
        let request_type;
        if (controlState.create_task_flag) {
            request_type = "POST"
        }
        if (controlState.edit_task_flag) {
            request_type = "PATCH"
            taskData._id = popupTask._id
        }
        await sendRequest(request_type, taskData);
        closePopup();
    };

    useEffect(() => {
        if (getInputData) {
            // Grab data from inputs
            const taskData = {
                title: document.getElementById('taskTitle').value,
                description: document.getElementById('taskDescription').value,
                members_ids: document.getElementById('taskMembers').value,
                due_date: document.getElementById('dueDate').value
            };
            console.log(taskData.title.length)
            if (taskData.title.length > 0) {
                handleSendData(taskData);
            } else {
                setGetInputData(false);
            }
        }
    }, [getInputData, handleSendData]);

    return (
        <div>
            {showPopup ? (
                <div>
                    <TaskItemPopup task={popupTask} />
                    <button onClick={handleCancel}>Cancel</button>
                    <button onClick={handleSave}>Save</button>
                </div>
            ) : (
                <div className={"task_board"}>
                    <TaskList state={controlState} showPopupCb={handlePopup} />
                    <TaskListControl changeState={handleChangeState} />
                </div>
            )}
        </div>
    );
};

export default TaskBoard;