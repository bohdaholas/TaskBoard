import React, { useEffect, useState } from 'react';
import TaskItem from "./TaskItem";

const TaskList = ({ state, showPopupCb }) => {
    const [tasks, setTasks] = useState([]);
    const facade_endpoint = 'http://localhost:2000'

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch(facade_endpoint);
                const raw_tasks = await response.text();
                setTasks(JSON.parse(raw_tasks));
            } catch (error) {
                console.error('Error fetching tasks:', error);
            }
        };
        fetchData();
    }, []);

    useEffect(() => {
        if (state.create_task_flag) {
            console.log("popup create");
            showPopupCb(
                { _id: "", title: "", description: "", members_ids: "", due_date: ""}
            )
        }
    }, [showPopupCb, state]);

    const handleRemoveTask = async (task) => {
        try {
            const response = await fetch(facade_endpoint, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({_id: task._id}),
            });
            if (response.ok) {
                setTasks((prevTasks) =>
                    prevTasks.filter((prevTask) => prevTask._id !== task._id));
                console.log('Delete request successful');
            } else {
                console.error('Delete request failed');
            }
        } catch (error) {
            console.error('Error occurred during delete request:', error);
        }
    }

    const taskClickCb = async (task) => {
        console.log(state)
        if (state.remove_task_flag) {
            await handleRemoveTask(task);
        }
        if (state.edit_task_flag) {
            console.log("edit popup")
            showPopupCb(task);
        }
    };

    return (
        <ul className="task_list">
            {tasks.map((task, index) => (
                <TaskItem key={index} task={task} onTaskClick={taskClickCb} />
            ))}
        </ul>
    );
}

export default TaskList;
