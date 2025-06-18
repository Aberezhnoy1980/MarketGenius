import { useRef, useEffect } from "react";
import { createPortal } from "react-dom";
import classes from "./Modal.module.css";

export default function Modal({ children, open }) {
	const dialog = useRef();

	useEffect(() => {
		if (open) {
			dialog.current.showModal();
			dialog.current.scrollTop = 0;
		} else {
			dialog.current.close();
		}
	}, [open]);

	return createPortal(
	// <dialog ref={dialog} className={classes.dialog} open={open}>
	<dialog className={classes.dialog} ref={dialog}>
		{children}
	</dialog>,
	document.getElementById("modal")
	);
}
