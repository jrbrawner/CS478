import * as React from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import CardHeader from '@mui/material/CardHeader';
import { red } from '@mui/material/colors';
import { useState } from 'react';
import { createComment } from '../../src/features/comments/commentSlice';
import { styled } from '@mui/material/styles';
import { useDispatch } from 'react-redux';
import { toast } from 'react-toastify';

import Box from '@mui/material/Box';
export default function CommentForm(props) {
	const dispatch = useDispatch();
	const [commentFormData, setCommentFormData] = useState({
		postId: props.postData._id,
		comment: '',
	});
	const { comment } = commentFormData;
	const handleInputChange = (e) => {
		const { name, value } = e.currentTarget;
		setCommentFormData((prevData) => ({
			...prevData,
			[name]: value,
		}));
	};
	const onFormSubmit = (e) => {
		e.preventDefault();
		if (!comment) {
			toast.error('Please enter a text.');
		} else {
			dispatch(createComment(commentFormData));
			setCommentFormData({
				postId: props.postData._id,
				comment: '',
			});
		}
	};
	return (
		<Box component='form' onSubmit={onFormSubmit} noValidate autoComplete='off'>
			<CardHeader
				avatar={
					<Avatar sx={{ bgcolor: red[500], width: 30, height: 30, mt: -5 }}>
						R
					</Avatar>
				}
				title={
					<TextField
						id='comment'
						name='comment'
						label='Write your comment here...'
						variant='filled'
						onChange={handleInputChange}
						value={comment}
						size='small'
						fullWidth
					/>
				}
				subheader={
					<Button
						variant='outlined'
						type='submit'
						sx={{ float: 'right', mt: 2 }}
					>
						Post
					</Button>
				}
			/>
		</Box>
	);
}