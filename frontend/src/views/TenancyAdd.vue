<template>
<div id="tenancy-add">
  <div class="tenant-names">
    <div class="table-container">
      <table class="table tenant-list">
        <thead>
          <th scope="col">Tenant Name</th>
          <th scope="col"></th>
        </thead>
        <tbody>
          <tr v-for="tenantField in tenantNames.tenantFields" v-bind:key="tenantField.name">
            <td>
              <input type="text" v-model="tenantField.value" v-bind:name="tenantField.name">
            </td>
            <td>
              <div class="btn btn-normal" v-on:click="deleteTenant(tenantField.name)">
                Delete
              </div>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <div class="btn btn-normal" v-on:click="addTenant()">
            Add Tenant
          </div>
        </tfoot>
      </table>
    </div>
  </div>
  <div class="date-range">
    <div class="start-date">
      <label>Start Date:</label>
      <input type="text" v-model="dateRange.startDate">
    </div>
    <div class="end-date">
      <label>End Date:</label>
      <input type="text" v-model="dateRange.endDate">
    </div>
  </div>
  <div class="rent-payment">
    <div>
      <label>Payment Terms:</label>
    </div>
    <div>
      <select v-on:change="paymentTermsChange($event)">
        <option value="0" selected="selected" disabled>
          -- Please select your payment terms --
        </option>
        <option v-for="paymentTerms in rentPayment.paymentTermsList"
        v-bind:key="paymentTerms.name" v-bind:value="paymentTerms.value">
          {{ paymentTerms.value }}
        </option>
      </select>
    </div>
    <div>
      <label>Rent Cost (AUD):</label>
    </div>
    <div>
      $ <input type="number" v-model="rentPayment.rentCost">&nbsp;
      <label v-if="rentPayment.selectedPaymentTerms != '0'">
        {{ rentPayment.selectedPaymentTerms }}
      </label>
    </div>
    <div>
      <label>Payment Method Description:</label>
    </div>
    <div>
      <textarea v-model="rentPayment.paymentDescription"></textarea>
    </div>
  </div>
  <div class="property-details">
    <div>
      <label>Property Address:</label>
    </div>
    <div>
      <input type="text" v-model="propertyDetails.propertyAddress">
    </div>
    <div>
      <label>Rent Type:</label>
    </div>
    <div>
      <select v-on:change="rentTypeChange($event)">
        <option value="0" selected="selected" disabled>
          -- Please select a rent type --
        </option>
        <option v-for="rentType in propertyDetails.rentTypeList"
        v-bind:key="rentType.name" v-bind:value="rentType.value">
          {{ rentType.value }}
        </option>
      </select>
    </div>
    <div v-if="propertyDetails.selectedRentType == 'Private Rooms'">
      <div>
        <label>Room Name:</label>
      </div>
      <div>
        <input type="text" v-model="propertyDetails.roomName">
      </div>
    </div>
  </div>
  <div class="notification-scheduling">
    <div class="table-container">
      <table class="table notification-list">
        <thead>
          <th>
            Notifications
          </th>
          <th>
            Days in advance of rent due date
          </th>
          <th>
          </th>
        </thead>
        <tbody>
          <tr v-for="notificationField in notifications.notificationFields"
          v-bind:key="notificationField.name">
            <td>
              Notification {{ notificationField.name }}
            </td>
            <td>
              <select v-on:change="notificationChange($event, notificationField.name)"
              v-bind:value="notificationField.value">
                <option v-for="day in notifications.days" v-bind:key="day">{{ day }}</option>
              </select>
            </td>
            <td>
              <div class="btn btn-normal" v-on:click="deleteNotification(notificationField.name)">
                Delete
              </div>
            </td>
          </tr>
        </tbody>
        <tfoot>
          <div class="btn" v-on:click="addNotification()">Add Nofication Schedule</div>
        </tfoot>
      </table>
    </div>
  </div>
  <div class="submit-buttons">
    <div class="btn" v-on:click="submitNewTenancy()">Submit</div>
  </div>
</div>
</template>

<script>
import tenancyAPI from '@/_api/tenancy';

export default {
  name: 'tenancy-add',
  data() {
    return {
      tenantNames: {
        tenantFields: [],
        tenantFieldIndex: 0,
      },
      dateRange: {
        startDate: '',
        endDate: '',
      },
      rentPayment: {
        paymentTermsList: [
          { name: 'Per week', value: 'Per week' },
          { name: 'Per fortnight', value: 'Per fortnight' },
          { name: 'Per month', value: 'Per month' },
        ],
        selectedPaymentTerms: '0',
        paymentDescription: '',
      },
      propertyDetails: {
        propertyAddress: '',
        rentTypeList: [
          { name: 'Whole Property', value: 'Whole Property' },
          { name: 'Private Rooms', value: 'Private Rooms' },
        ],
        selectedRentType: '0',
        roomName: '',
      },
      notifications: {
        notificationFields: [],
        notificationFieldIndex: 0,
        days: Array(14).fill().map((_, i) => i + 1),
      },
    };
  },
  methods: {
    submitNewTenancy() {
      const vm = this;
      tenancyAPI.addNewTenancy({
        tenants: this.tenantNames.tenantFields.map(
          tenantField => tenantField.value,
        ),
        tenancy: {
          start_date: this.dateRange.startDate,
          end_date: this.dateRange.endDate,
          address: this.propertyDetails.propertyAddress,
          rent_type: this.propertyDetails.selectedRentType,
          room_name: (
            this.propertyDetails.selectedRentType === 'Private Rooms'
          ) ? this.propertyDetails.roomName : null,
          payment_terms: this.rentPayment.selectedPaymentTerms,
          rent_cost: this.rentPayment.rentCost,
          payment_description: this.rentPayment.paymentDescription,
        },
        notifications: this.notifications.notificationFields.map(
          notificationField => notificationField.value,
        ),
      }, () => {
        vm.$router.push('/');
      }, (error) => {
        console.log(['failure:', error].join(' '));
      });
    },
    addTenant() {
      this.tenantNames.tenantFields.push({
        name: this.tenantNames.tenantFieldIndex,
        value: '',
      });
      this.tenantNames.tenantFieldIndex += 1;
    },
    deleteTenant(name) {
      this.tenantNames.tenantFields = this.tenantNames.tenantFields.filter(
        tenantField => tenantField.name !== name,
      );
    },
    paymentTermsChange(event) {
      this.rentPayment.selectedPaymentTerms = event.target.value;
    },
    paymentMethodChange(event) {
      this.rentPayment.selectedPaymentMethod = event.target.value;
    },
    rentTypeChange(event) {
      this.propertyDetails.selectedRentType = event.target.value;
    },
    addNotification() {
      this.notifications.notificationFields.push({
        name: this.notifications.notificationFieldIndex,
        value: 7,
      });
      this.notifications.notificationFieldIndex += 1;
    },
    notificationChange(event, notificationFieldName) {
      this.notifications.notificationFields.find(
        notification => notification.name === notificationFieldName,
      ).value = parseInt(event.target.value, 10);
    },
    deleteNotification(name) {
      this.notifications.notificationFields = this.notifications.notificationFields.filter(
        notificationField => notificationField.name !== name,
      );
    },
  },
};
</script>
