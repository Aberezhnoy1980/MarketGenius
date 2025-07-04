import React, { useState } from "react";
import classes from "./Preorder.module.css";
import Modal from "../Modal/Modal";
import Button from "../Button/Button";
import { useNavigate, Link } from "react-router-dom";

const Preorder = () => {
	const [isAccepted, setIsAccepted] = useState(false);
	const [modal, setModal] = useState(false);
	const navigate = useNavigate();

	// const buyAccess = () => {
	// 	alert(
	// 		"Оплата будет доступна позже. Пожалуйста, следите за обновлениями."
	// 	);
	// };
	return (
		<>
			<div id="modal"></div>
			<div className={classes.container}>
				<Modal open={modal}>
					<div className={classes.modal_content}>
						<h2>
							Публичная оферта на оказание информационных услуг
						</h2>
						<p>
							<strong>1. Предмет договора</strong>
							<br />
							1.1. Исполнитель обязуется предоставить Пользователю
							доступ к информационному сервису «Market Genius»,
							содержащему аналитические и справочные материалы, а
							также программные функции для самостоятельного
							анализа акций Московской биржи.
							<b />
							1.2. Сервис находится в стадии разработки (MVP),
							отдельные функции могут предоставляться поэтапно.
							<br />
							1.3. Услуга считается оказанной в момент
							предоставления доступа в личный кабинет
							Пользователя.
						</p>
						<p>
							<strong>2. Порядок предоставления доступа</strong>
							<br />
							2.1. После оплаты Пользователь получает уникальные
							данные для авторизации в личном кабинете сервиса.
							<br />
							2.2. Доступ к сервису будет предоставлен не позднее
							01.06.2025. До этой даты передача доступа не
							осуществляется, даже при успешной оплате.
							<br />
							2.3. Регистрация и вход осуществляются без
							предоставления персональных данных.
						</p>
						<p>
							<strong>3. Стоимость и порядок оплаты</strong>
							<br />
							3.1. Стоимость ежемесячной подписки составляет 1990
							рублей.
							<br />
							3.2. Оплата осуществляется через платёжные системы.
							<br />
							3.3. Моментом оплаты считается зачисление средств на
							расчётный счёт Исполнителя.
						</p>
						<p>
							<strong>4. Права и обязанности сторон</strong>
							<br />
							4.1. Исполнитель обязуется предоставить доступ к
							сервису в заявленный срок.
							<br />
							4.2. Пользователь обязуется использовать доступ
							только в личных целях.
							<br />
							4.3. Исполнитель вправе вносить изменения в
							интерфейс и функционал сервиса без предварительного
							уведомления.
							<br />
							4.4. Исполнитель не гарантирует достижение
							Пользователем каких-либо результатов.
						</p>
						<p>
							<strong>5. Ограничение ответственности</strong>
							<br />
							5.1. Вся информация носит демонстрационный характер
							и не является инвестиционной рекомендацией.
							<br />
							5.2. Сервис не осуществляет брокерскую или дилерскую
							деятельность.
							<br />
							5.3. Исполнитель не несёт ответственности за
							решения, принятые Пользователем на основе информации
							из сервиса.
							<br />
							5.4. Исполнитель не несёт ответственности за
							полноту, актуальность, точность или прикладную
							пригодность представленной информации. Все данные и
							аналитика являются оценочными и информативными,
							могут основываться на автоматической обработке и
							интерпретациях, и не претендуют на объективность или
							исключительную корректность.
						</p>
						<p>
							<strong>6. Возврат средств</strong>
							<br />
							6.1. После активации доступа возврат денежных
							средств невозможен.
							<br />
							6.2. При технических сбоях доступ продлевается по
							запросу.
						</p>
						<p>
							<strong>7. Использование cookie и аналитики</strong>
							<br />
							7.1. Используется Яндекс.Метрика и другие
							технологии.
							<br />
							7.2. Персональные данные не обрабатываются.
							<br />
							7.3. Пользователь соглашается с cookie, продолжая
							пользоваться сайтом.
							<br />
							7.4. Подробнее: https://yandex.ru/legal/confidential
						</p>
						<p>
							<strong>
								8. Особые условия конфиденциальности
							</strong>
							<br />
							8.1. Персональные данные не собираются.
							<br />
							8.2. Восстановление доступа невозможно без ПД.
							<br />
							8.3. Ответственность за логин/пароль несёт
							Пользователь.
							<br />
							8.4. Новый доступ возможен только при новой оплате.
						</p>
						<p>
							<strong>9. Принятие условий оферты</strong>
							<br />
							9.1. Оплата или подтверждение условий оферты
							означает акцепт.
							<br />
							9.2. Актуальная редакция публикуется на сайте и
							может быть изменена без уведомления.
						</p>
						<p>
							<strong>
								10. Контактная информация и реквизиты
							</strong>
							<br />
							ФИО: Михайлова Мария Александровна
							<br />
							ИНН: 781696602568
							<br />
							Контакт: @MrktGns
						</p>
						<Button
							className={classes.button}
							onClick={() => setModal(false)}>
							Вернуться
						</Button>
					</div>
				</Modal>
				<h1>Market Genius</h1>

				<div className="block">
					<p>
						<strong>
							Платформа для анализа акций с помощью искусственного
							интеллекта
						</strong>
					</p>
					<p>
						⚙️ <strong>Сервис в стадии запуска</strong>. Старт
						доступа — <strong>1 июня 2025</strong>.
					</p>
				</div>

				<div className="block">
					<h3>💰 Стоимость подписки</h3>
					<p>
						Месячный доступ — <strong>1990 ₽</strong>
					</p>
					<div className="checkbox-container">
						<input
							type="checkbox"
							id="accept"
							checked={isAccepted}
							onChange={(e) => setIsAccepted(e.target.checked)}
						/>
						<label htmlFor="accept">
							Я принимаю{" "}
							<a href="#" onClick={() => setModal(true)}>
								условия публичной оферты
							</a>
						</label>
					</div>
					<div style={{ marginTop: "20px" }}>
						<button
							className={classes.button}
							style={{ padding: "10px 18px", fontSize: "14px" }}
							onClick={navigate('/register')}
							disabled={!isAccepted}>
							Купить доступ
						</button>
					</div>
				</div>

				<div className={classes.block}>
					<h3>📈 Что вы получите:</h3>
					<ul>
						<li>
							Обобщённую аналитическую информацию по акциям
							Мосбиржи
						</li>
						<li>Аналитику рыночной тональности новостного фона</li>
						<li>Обобщённые мнения экспертов</li>
						<li>
							Персональный доступ в информационную систему сервиса
						</li>
					</ul>
				</div>

				<div
					style={{
						display: "flex",
						justifyContent: "center",
						marginTop: "20px",
					}}>
					{/* <button
						className={classes.button}
						style={{ padding: "10px 18px", fontSize: "14px" }}
						onClick={buyAccess}>
						Попробывать бета-версию
					</button> */}
				</div>

				<div className={classes.footer}>
					<p>
						Платформа Market Genius не осуществляет брокерскую,
						дилерскую деятельность и не имеет лицензии на
						инвестиционное консультирование.
					</p>
				</div>
			</div>
		</>
	);
};

export default Preorder;
